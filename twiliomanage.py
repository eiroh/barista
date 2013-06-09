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
import define

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

class twiliomanage(sqlitedb):

    def _get_twilio(self):
        account = '%s' % options_account
        token = '%s' % options_token
        client = TwilioRestClient(account, token)
        return client

    def _paralellcall(self, eventinfo, callinfo):
        sid = define.INITIAL_VALUE['callsid']
        if eventinfo['testflg'] == int(define.DEBUG_FLG['off']):
            call = self._get_twilio().calls.create(to='%s' % options_to, from_='%s' % options_from_, url='%s:%s/callresponse?eventid=%s' % (options_baseurl, options_port, eventinfo['eventid']))
            sid = call.sid
        result = sqlitedb.insertsid(self, eventinfo['eventid'], callinfo['numorder'], callinfo['ghid'], sid)
        return

    def _sequentialcall(self, eventinfo, callinfo):
        print 'seuential call: we havent supported yet'
        return

    def callrequest(self, eventid):
        event_info = sqlitedb.geteventinfo(self, eventid)
        eventinfo = event_info[0]
        callinfo = sqlitedb.getactivecall(self, eventid)
        result = self._isalive(eventinfo, callinfo)
        if result == True:
            if eventinfo['calltype'] == int(define.CALL_TYPE['paralell']):
                resutl = self._paralellcall(eventinfo, callinfo)
            else:
                result = self._sequentialcall(eventinfo, callinfo)
            return result
        else:
            return

    def _isalive(self, eventinfo, callinfo):
        for call in callinfo:
            if eventinfo['frequency'] > call['attempt']:
                return True
        result = sqlitedb.finishevent(self, eventinfo)
        return False

    def announce(self, eventid):
        result = sqlitedb.geteventinfo(self, eventid)
        record = result[0]
        message = record['message'].encode('utf-8')
        text1 = '<?xml version="1.0" encoding="UTF-8"?>\n'
        text2 = '<Response><Gather action=\"./status\" method=\"post\" timeout=\"10\">'
        text3 = '<Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">'
        text4 = '%s%s%s' % (options_headid1, message, options_footid1)
        text5 = '</Say></Gather><Say voice=\"woman\" language=\"ja-jp\" loop=\"1\">%s</Say></Response>' % options_response_timeout
        result = '%s%s%s%s%s' % (text1, text2, text3, text4, text5)
        return result

    def response(self, digits):
        text = options_response_timeout
        if digits != '' and digits == define.PUSHED_DIGITS['positive']:
            text = options_response_positive
        elif digits != '' and digits == define.PUSHED_DIGITS['negative']:
            text = options_response_negative
        elif digits != '':
            text = options_response_unknown
        head = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        result = '%s<Response><Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">%s、%s</Say></Response>' % (head, text, options_response_end)
        return result

    def get_record(self, callsid):
        print '%s' % callsid 
        call = self._get_twilio().calls.get(callsid)
        result = 'status=%s start_time=%s' % (call.status, call.start_time)
        return result
