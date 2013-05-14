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
import ConfigParser
from twiliomanage import twiliomanage

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
options_baseurl = conf.get('Tornado', 'baseurl')
options_port    = conf.get('Tornado', 'port')
options_from_   = conf.get('Twilio', 'from_')
options_to      = conf.get('Twilio', 'to')
options_account = conf.get('Twilio', 'account')
options_token   = conf.get('Twilio', 'token')
options_resqserver = conf.get('ResQ', 'server')
options_resqport   = conf.get('ResQ', 'port')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/call', CallHandler),
            (r'/status', StatusHandler),
            (r'/callresponse', CallResponseHandler),
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
        account = '%s' % options_account
        token = '%s' % options_token
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
        lastnum = 0
        addressee = self.request.arguments['addressee']
        db = sqlitedb()
        eventid = db.geteventid()
        status = 1
        result = db.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid, lastnum)
        for record in addressee:
            param = record.split(':')
            numorder = param[0]
            ghid = param[1]
            telno = param[2]
            name = param[3]
            callid = 0
            attempt = 0
            latesttime = 0
            lateststatus = 1
            result = db.callregister(eventid, numorder, ghid, name, telno, callid, attempt, latesttime, lateststatus)
        r = ResQ(server="%s:%s" % (options_resqserver, options_resqport))
        r.enqueue(eventQ, eventid)
        response = '{\"success\":\"true\",\"eventid\":\"123\"}'
        self.set_header("Content-Type", "application/json;charset=utf-8")
        self.write(response)

    def get(self):
        result = 'OK'
        self.render("eventhandler.html", result=result)

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

    def get(self):
        sid = self.get_argument('sid')
        tw = twiliomanage()
        result = tw.get_record(sid)
        self.write(result)

class CallResponseHandler(BaseHandler):
    def post(self):
        tw = twiliomanage()
        result = tw.announce()
        self.write(result)

class StatusHandler(BaseHandler):
    def post(self):
        print 'StatusHandler method=post'
        Digits = self.get_argument('Digits')
        print Digits
        tw = twiliomanage()
        result = tw.response(Digits)
        self.write(result)

    def get(self):
        print 'StatusHandler method=get'
        CallSid = self.get_argument('CallSid')
        tw = twilio()
        result = tw.get_record(CallSid)
        self.write(result)

def main():
    tornado.options.parse_command_line()
    db = sqlitedb()
    db.initdb()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
