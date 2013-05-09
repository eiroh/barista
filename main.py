#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import logging
import string
import time
import uuid
from optparse import OptionParser
import os, sys
import time
from os import path
from tornado.options import define, options
from datetime import datetime
import json
from pyres import ResQ
from eventq import eventQ
from twilio.rest import TwilioRestClient
from twilio import twiml
from dbmanage import sqlitedb

define("port", default=7776, help="run on the given port", type=int)
define('baseurl', default='http://hoge.example.com:7776', help='callback url')
define('from_', default='+81', help='phone number call from')
define('to', default='+81', help='destination phone number')
define('account', default='hoge', help='your account of twilio')
define('token', default='hoge', help='your token of twilio')
define('initdb', default=False, help='create table', type=bool)
define('resqserver', default='localhost', help='ResQ redis server')
define('resqport', default=6379, help='ResQ redis port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/call', CallHandler),
            (r'/status', StatusHandler),
            (r'/callresponse', CallResponseHandler),
            (r'/', EventIndexHandler),
            (r'/event', EventHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        tornado.options.parse_command_line()

class BaseHandler(tornado.web.RequestHandler):
    def get_twilio(self):
        account = '%s' % options.account
        token = '%s' % options.token
        client = TwilioRestClient(account, token)
        return client

class EventHandler(BaseHandler):
    def post(self):
        testflg = self.get_argument('testflg')
        hostname = self.get_argument('hostname')
        operator = self.get_argument('operator')
        calltype = self.get_argument('calltype')
        frequency = self.get_argument('frequency')
        message = self.get_argument('message')
        headid = self.get_argument('headid')
        footid = self.get_argument('footid')
        lastnum = self.get_argument('lastnum')
        addressee = self.request.arguments['addressee']
        db = sqlitedb()
        eventid = db.geteventid()
        status = 'init'
        result = db.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid, lastnum)
        for record in addressee:
            param = record.split(':')
            numorder = param[0]
            ghid = param[1]
            telno = param[2]
            name = param[3]
            callid = 'init'
            attempt = 0
            latesttime = 'init'
            lateststatus = 'init'
            result = db.callregister(eventid, numorder, ghid, name, telno, callid, attempt, latesttime, lateststatus)
        r = ResQ(server="%s:%s" % (options.resqserver, options.resqport))
        r.enqueue(eventQ, eventid)
        self.write('OK')

class CallHandler(BaseHandler):
    def post(self):
        testflg = self.get_argument('testflg')
        hostname = self.get_argument('hostname')
        operator = self.get_argument('operator')
        calltype = self.get_argument('calltype')
        frequency = self.get_argument('frequency')
        message = self.get_argument('message')
        headid = self.get_argument('headid')
        footid = self.get_argument('footid')
        addressee = self.request.arguments['addressee']
        db = sqlitedb()
        eventid = db.geteventid()
        status = 'init'
        result = db.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid)
        self.write('OK')
        #call = self.get_twilio().calls.create(to='%s' % options.to, from_='%s' % options.from_, url='%s/callresponse' % options.baseurl)
        #self.write('OK callsid=%s' % call.sid)

    def get(self):
        sid = self.get_argument('sid')
        call = self.get_twilio().calls.get(sid)
        self.write('status=%s start_time=%s' % (call.status, call.start_time))

class CallResponseHandler(BaseHandler):
    def post(self):
        text1 = '<?xml version="1.0" encoding="UTF-8"?>\n'
        text2 = '<Response><Gather action=\"./status\" method=\"post\" timeout=\"15\">'
        text3 = '<Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">'
        text4 = 'こちらは、おじぞうさんです。アラートを検知しました。サーバーめいは、hogehoge。Socket timeout after 10 secondsです。対応できる場合は1を、できない場合は2をプッシュしてください。'
        text5 = '</Say></Gather><Say voice=\"woman\" language=\"ja-jp\" loop=\"1\">プッシュ操作が確認できませんでした。</Say></Response>'
        self.write('%s%s%s%s%s' % (text1, text2, text3, text4, text5))

class StatusHandler(BaseHandler):
    def post(self):
        print 'StatusHandler method=post'
        CallSid = self.get_argument('CallSid')
        print CallSid
        CallStatus = self.get_argument('CallStatus')
        print CallStatus
        Digits = self.get_argument('Digits')
        print Digits
        head = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        text = 'プッシュ操作なし'
        if Digits != '' and Digits == '1':
            text = '対応できる'
        elif Digits != '' and Digits == '2':
            text = '対応できない' 
        elif Digits != '':
            text = '無効な番号'
        self.write('%s<Response><Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">%s、を登録しました。</Say></Response>' % (head, text))

    def get(self):
        print 'StatusHandler method=get'
        CallSid = self.get_argument('CallSid')
        print CallSid
        CallStatus = self.get_argument('CallStatus')
        print CallStatus
        self.write('%s' % CallSid)

class EventIndexHandler(BaseHandler):
    def get(self):
        print 'hoge'
        self.render("index.html")

def main():
    tornado.options.parse_command_line()
    print options.initdb
    if options.initdb == True:
        db = sqlitedb()
        db.initdb()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
