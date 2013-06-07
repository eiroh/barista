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
conf.read('settings.ini')
options_resqserver = conf.get('ResQ', 'server')
options_resqport   = conf.get('ResQ', 'port')

class barista():

    def firstRegist(self, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, addressee):

        tw = twiliomanage()
        eventid = tw.geteventid()
        status = define.EVENT_STATUS['WAITING']
        lastnum = 0
        tw.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum)
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
            lateststatus = define.CALL_STATUS['WAITING']
            tw.callregister(eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus)
        r = ResQ(server="%s:%s" % (options_resqserver, options_resqport))
        r.enqueue(eventQ, eventid)
        return eventid
