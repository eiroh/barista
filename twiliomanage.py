#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import os, sys
from twilio.rest import TwilioRestClient
from twilio import twiml
import ConfigParser
from dbmanage import sqlitedb
import define

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
options_from_   = conf.get('Twilio', 'from_')
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

    def _call(self, eventinfo, callinfo):
        sid = define.INITIAL_VALUE['callsid']
        if eventinfo['testflg'] == int(define.DEBUG_FLG['off']):
            for cinfo in callinfo:
                call = self._get_twilio().calls.create \
                    (to='%s' % cinfo['telno'], from_='%s' % options_from_, url='%s:%s/callresponse?eventid=%s&numorder=%s&ghid=%s' % \
                    (options_baseurl, options_port, eventinfo['eventid'], cinfo['numorder'], cinfo['ghid']))
                sid = call.sid
                result = sqlitedb.insertsid(self, eventinfo['eventid'], cinfo['numorder'], cinfo['ghid'], sid)
        return

    def callrequest(self, eventid):
        events = sqlitedb.geteventinfo(self, eventid)
        for event in events:
            calls = sqlitedb.getactivecall(self, eventid, int(event['frequency']))
            print calls
            if calls == '':
                result = sqlitedb.finishevent(self, event)
            else:
                if event['calltype'] == int(define.CALL_TYPE['paralell']):
                    print 'paralell proc'
                    self._call(event, calls)
                else:
                    print 'sequential call'
                    call = calls[0]
                    self._call(event, call)
        return

    def announce(self, eventid, numorder, ghid):
        result = sqlitedb.geteventinfo(self, eventid)
        record = result[0]
        language = record['language'].encode('utf-8')
        message = record['message'].encode('utf-8')
        text1 = '<?xml version="1.0" encoding="UTF-8"?>\n'
        text2 = '<Response><Gather action=\"./status/%s/%s/%s\" method=\"POST\" timeout=\"10\" numDigits=\"1\">' % \
                (eventid.encode('utf-8'), numorder.encode('utf-8'), ghid.encode('utf-8'))
        text3 = '<Say voice=\"woman\" language=\"%s\" loop=\"2\">' % language
        text4 = '%s%s%s' % (options_headid1, message, options_footid1)
        text5 = '</Say></Gather><Say voice=\"woman\" language=\"%s\" loop=\"2\">%s</Say></Response>' % (language, options_response_timeout)
        result = '%s%s%s%s%s' % (text1, text2, text3, text4, text5)
        print '%s' % result
        return result

    def response(self, digits, eventid, numorder, ghid, callsid):
        print '%s,%s,%s,%s,%s' % (digits, eventid, numorder, ghid, callsid)
        text = options_response_timeout
        if digits != '' and digits == define.PUSHED_DIGITS['positive']:
            text = options_response_positive
        elif digits != '' and digits == define.PUSHED_DIGITS['negative']:
            text = options_response_negative
        elif digits != '':
            digits = define.ANSWER_STATUS['UNKNOWN_ERROR']
            text = options_response_unknown
        head = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        result = '%s<Response><Say voice=\"woman\" language=\"%s\" loop=\"2\">%s、%s</Say></Response>' % (head, 'ja-jp', text, options_response_end)
        dbresult = sqlitedb.updatelateststatus(self, callsid, digits)
        return result

    def get_record(self, callsid):
        print '%s' % callsid 
        call = self._get_twilio().calls.get(callsid)
        result = 'status=%s start_time=%s' % (call.status, call.start_time)
        return result
