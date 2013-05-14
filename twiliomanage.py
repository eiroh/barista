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

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
options_from_   = conf.get('Twilio', 'from_')
options_to      = conf.get('Twilio', 'to')
options_account = conf.get('Twilio', 'account')
options_token   = conf.get('Twilio', 'token')
options_baseurl = conf.get('Tornado', 'baseurl')
options_port    = conf.get('Tornado', 'port')

class twiliomanage():

    def get_twilio(self):
        account = '%s' % options_account
        token = '%s' % options_token
        client = TwilioRestClient(account, token)
        return client

    def call(self, ghid, name, telno, testflg, hostname, message, headid, footid):
        call = self.get_twilio().calls.create(to='%s' % options_to, from_='%s' % options_from_, url='%s:%s/callresponse' % (options_baseurl, options_port))
        print 'OK callsid=%s' % call.sid
        return call.sid

    def announce(self):
        text1 = '<?xml version="1.0" encoding="UTF-8"?>\n'
        text2 = '<Response><Gather action=\"./status\" method=\"post\" timeout=\"15\">'
        text3 = '<Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">'
        text4 = 'こちらは、バリスタです。アラートを検知しました。サーバーめいは、hoge.example.com。Socket timeout after 10 secondsです。対応できる場合は1を、できない場合は2をプッシュしてからシャープを>プッシュしてください。'
        text5 = '</Say></Gather><Say voice=\"woman\" language=\"ja-jp\" loop=\"1\">プッシュ操作が確認できませんでした。</Say></Response>'
        result = '%s%s%s%s%s' % (text1, text2, text3, text4, text5)
        return result

    def response(self, digits):
        print digits
        head = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n'
        text = 'プッシュ操作なし'
        if digits != '' and digits == '1':
            text = '対応できる'
        elif digits != '' and digits == '2':
            text = '対応できない'
        elif digits != '':
            text = '無効な番号'
        result = '%s<Response><Say voice=\"woman\" language=\"ja-jp\" loop=\"2\">%s、を登録しました。</Say></Response>' % (head, text)
        return result

    def get_record(self, callsid):
        print callsid
        print '%s' % callsid 
        call = self.get_twilio().calls.get(callsid)
        result = 'status=%s start_time=%s' % (call.status, call.start_time)
        return result
