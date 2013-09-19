#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import logging
import string
from optparse import OptionParser
import os, sys
from os import path
from tornado.options import define, options
import ConfigParser
from twiliomanage import twiliomanage
import define
from barista import barista

conf = ConfigParser.SafeConfigParser()
conf.read('./barista/settings.ini')
options_baseurl = conf.get('Tornado', 'baseurl')
options_port    = conf.get('Tornado', 'port')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/api/v1/call', EventHandler), # call request
            (r'/callresponse', CallResponseHandler), # response announcement
            (r'/status/([^/]+)/([^/]+)/([^/]+)', StatusHandler), # digit response
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=False,
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        tornado.options.parse_command_line()

class EventHandler(tornado.web.RequestHandler):

    def checkinput(self, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, addressee):
        if testflg != define.DEBUG_FLG['off'] and testflg != define.DEBUG_FLG['on']:
           logging.info('input parameter error testflg')
           return False
        if hostname == '':
           logging.info('input parameter error hostname')
           return False
        if operator == '':
           logging.info('input parameter error operator')
           return False
        if calltype != define.CALL_TYPE['sequential'] and calltype != define.CALL_TYPE['paralell']:
           logging.info('input parameter error calltype')
           return False
        if int(frequency) > int(define.MAX_NUM_OF_CALL):
           logging.info('input parameter error frequency')
           return False
        if language != 'en' and language != 'ja-jp':
           logging.info('input parameter error language')
           return False
        if message == '':
           logging.info('input parameter error message')
           return False
        if headid != '1' and headid != '2':
           logging.info('input parameter error headid')
           return False
        if footid != '1' and footid != '2':
           logging.info('input parameter error footid')
           return False
        for record in addressee:
           param = record.split(':')
           if len(param) != 5:
               logging.info('input parameter error addressee')
               return False
           numorder = param[0]
           if int(numorder) > int(define.MAX_NUM_OF_ADDRESSEE):
               logging.info('input parameter error numorder')
               return False
           ghid = param[1]
           if ghid == '':
               logging.info('input parameter error ghid')
               return False
           telno = param[2]
           if telno == '':
               logging.info('input parameter error telno')
               return False
           name = param[3]
           if name == '':
               logging.info('input parameter error name')
               return False
           sleep = param[4]
           if int(sleep) > int(define.MAX_SEC_OF_SLEEP):
               logging.info('input parameter error sleep')
               return False
        return True

    def post(self):

        testflg = self.get_argument('testflg')
        hostname = self.get_argument('hostname')
        operator = self.get_argument('operator')
        calltype = self.get_argument('calltype')
        frequency = self.get_argument('frequency')
        language = self.get_argument('language')
        message = self.get_argument('message')
        headid = self.get_argument('headid')
        footid = self.get_argument('footid')
        addressee = self.request.arguments['addressee']

        self.set_header("Content-Type", "application/json;charset=utf-8")
        result = self.checkinput(testflg, hostname, operator, calltype, frequency, language, message, headid, footid, addressee)
        if result == False:
            response = '{\"success\":\"false\",\"error\":\"%s\"}' % define.ERROR_CODE['parameters']
            self.write(response)
        else:
            main = barista()
            eventid = main.firstRegist(testflg, hostname, operator, calltype, frequency, language, message, headid, footid, addressee)
            if eventid == '':
                response = '{\"success\":\"false\",\"error\":\"%s\"}' % define.ERROR_CODE['connection']
                self.write(response)
            response = '{\"success\":\"true\",\"eventid\":\"%s\"}' % eventid
            self.write(response)

    def get(self):

        eventid = self.get_argument('eventid')
        self.set_header("Content-Type", "application/json;charset=utf-8") 
        if eventid == '':
            logging.info('input parameter error testflg')
            response = '{\"success\":\"false\",\"error\":\"%s\"}' % define.ERROR_CODE['parameters']
        else:
            main = barista()
            result = main.getLog(eventid)
        self.write(result)

class CallResponseHandler(tornado.web.RequestHandler):
    def post(self):
        eventid = self.get_argument('eventid')
        numorder = self.get_argument('numorder')
        ghid = self.get_argument('ghid')
        tw = twiliomanage()
        result = tw.announce(eventid, numorder, ghid)
        self.write(result)

class StatusHandler(tornado.web.RequestHandler):
    def post(self, eventid, numorder, ghid): # called by twilio
        logging.info('StatusHandler method=post')
        Digits = self.get_argument('Digits')
        CallSid = self.get_argument('CallSid')
        tw = twiliomanage()
        result = tw.response(Digits, eventid, numorder, ghid, CallSid)
        self.write(result)

def main():
    tornado.options.parse_command_line()
    tw = twiliomanage()
    tw.initdb()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options_port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
