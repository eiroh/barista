#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import sqlite3
from twilio.rest import TwilioRestClient
from twilio import twiml
import ConfigParser
from dbmanage import sqlitedb

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
options_from_   = conf.get('Twilio', 'from_')
options_to      = conf.get('Twilio', 'to')
options_account = conf.get('Twilio', 'account')
options_token   = conf.get('Twilio', 'token')
options_baseurl = conf.get('Tornado', 'baseurl')
options_port    = conf.get('Tornado', 'port')
options_headid1 = conf.get('Barista', 'headid1')
options_headid2 = conf.get('Barista', 'headid2')
options_footid1 = conf.get('Barista', 'footid1')
options_footid2 = conf.get('Barista', 'footid2')
options_response_positive = conf.get('Barista', 'response_positive')
options_response_negative = conf.get('Barista', 'response_negative')
options_response_unknown  = conf.get('Barista', 'response_unknown')
options_response_nothing  = conf.get('Barista', 'response_nothing')
options_response_end      = conf.get('Barista', 'response_end')
options_response_timeout  = conf.get('Barista', 'response_timeout')

class twiliomanage():

    def get_twilio(self):
        account = '%s' % options_account
        token = '%s' % options_token
        client = TwilioRestClient(account, token)
        return client

    def call(self, eventid, numorder, ghid, name, telno, testflg, hostname, message, headid, footid):
        print 'eventid=%s, numorder=%s, ghid=%s, name=%s, telno=%s, testflg=%s, hostname=%s, message=%s, headid=%s, footid=%s' % (eventid, numorder, ghid, name, telno, testflg, hostname, message, headid, footid)
        sid = '0'
        if testflg == 1:
            sid = '1234567890'
        else:
            call = self.get_twilio().calls.create(to='%s' % options_to, from_='%s' % options_from_, url='%s:%s/callresponse?eventid=%s' % (options_baseurl, options_port, eventid))
            #call = self.get_twilio().calls.create(to='%s' % telno, from_='%s' % options_from_, url='%s:%s/callresponse?eventid=%s' % (options_baseurl, options_port, eventid))
            sid = call.sid
        db = sqlitedb()
        result = db.insertsid(eventid, numorder, ghid, sid)
        print 'twiliomanage::call'
        return '0'

    def announce(self, eventid):
        db = sqlitedb()
        result = db.geteventinfo(eventid)
        record = result[0]
        message = record[8].encode('utf-8')
        print message
        text1 = '<?xml version="1.0" encoding="UTF-8"?>\n'
        text2 = '<Response><Gather action=\"./status\" method=\"post\" timeout=\"10\">'
        text3 = '<Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">'
        text4 = '%s%s%s' % (options_headid1, message, options_footid1)
        text5 = '</Say></Gather><Say voice=\"woman\" language=\"ja-jp\" loop=\"1\">%s</Say></Response>' % options_response_timeout
        result = '%s%s%s%s%s' % (text1, text2, text3, text4, text5)
        return result

    def response(self, digits):
        print digits
        text = options_response_timeout
        if digits != '' and digits == '1':
            text = options_response_positive
        elif digits != '' and digits == '2':
            text = options_response_negative
        elif digits != '':
            text = options_response_unknown
        head = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        result = '%s<Response><Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">%s、%s</Say></Response>' % (head, text, options_response_end)
        return result

    def get_record(self, callsid):
        print callsid
        print '%s' % callsid 
        call = self.get_twilio().calls.get(callsid)
        result = 'status=%s start_time=%s' % (call.status, call.start_time)
        return result
