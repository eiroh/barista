#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import logging
import string
import time
from twiliomanage import twiliomanage
import define
import ConfigParser
from pyres import ResQ
from eventq import eventQ

conf = ConfigParser.SafeConfigParser()
conf.read('./barista/settings.ini')
options_resqserver = conf.get('ResQ', 'server')
options_resqport   = conf.get('ResQ', 'port')

class barista():

    def firstRegist(self, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, addressee):

        if headid == '1':
            headmsg = conf.get('Barista', 'headid1')
        else:
            headmsg = conf.get('Barista', 'headid2')

        if footid == '1':
            footmsg = conf.get('Barista', 'footid1')
        else:
            footmsg = conf.get('Barista', 'footid2')

        tw = twiliomanage()
        eventid = tw.geteventid()
        status = define.EVENT_STATUS['WAITING']
        lastnum = 0
        #tw.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum)
        tw.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, headmsg, footmsg, lastnum)
        for record in addressee:
            param = record.split(':')
            numorder = param[0]
            ghid = param[1]
            telno = param[2]
            name = param[3]
            sleep = param[4]
            callid = 0
            attempt = 0
            latesttime = 0
            lateststatus = define.ANSWER_STATUS['NORESPONSE']
            tw.callregister(eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus)
        r = ResQ(server="%s:%s" % (options_resqserver, options_resqport))
        r.enqueue(eventQ, eventid)
        return eventid

    def getLog(self, eventid):

        tw = twiliomanage()
        result = tw.getalllog(eventid)

        calldata = ''
        for i,record in enumerate(result['call']):
            if i != 0:
                calldata = calldata + ','
            data = '{\"ghid\":\"%s\", \"order\":\"%s\", \"telno\":\"%s\", \"name\":\"%s\", \"numofcall\":\"%s\", \"latestcall\":\"%s\", \"status\":\"%s\"}' % \
                    (record['ghid'], record['numorder'], record['telno'], record['name'], record['attempt'], record['latesttime'], record['lateststatus'])
            calldata = calldata + data
        #print calldata.encode('utf-8')

        response = '{\"success\":\"true\", \"type\":\"%s\", \"frequency\":\"%s\", \"language\":\"%s\", \"headid\":\"%s\", \"footid\":\"%s\", \"headmsg\":\"%s\", \"announce\":\"%s\", \"footmsg\":\"%s\", \"eventstatus\":\"%s\", \"result\":[%s]}' % \
                    (result['event'][0]['calltype'], \
                    result['event'][0]['frequency'], \
                    result['event'][0]['language'], \
                    result['event'][0]['headid'], \
                    result['event'][0]['footid'], \
                    result['event'][0]['headmsg'], \
                    result['event'][0]['message'], \
                    result['event'][0]['footmsg'], \
                    result['event'][0]['status'], \
                    calldata)
        return response

