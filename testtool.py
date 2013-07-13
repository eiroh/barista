# -*- coding: utf-8 -*-

import time
import sqlite3
from dbmanage import sqlitedb
from pyres import ResQ
from callq import callQ
import ConfigParser
from twiliomanage import twiliomanage
import sys
import define

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')

def main(tid):
    if tid == '1':
        tw = twiliomanage()
        tw.initdb()
        #testflg, hostname, operator, calltype, frequency, language, message, headid, footid, addressee

        testflg = 1
        hostname = 'test.example.com'
        operator = 'testuser'
        calltype = 1
        frequency = 2
        language = 'ja-jp'
        message = 'Socket timeout after 10 secondsです'
        headid = 1
        footid = 1

        addressee = []
        tmp = '1:tarou:810000000000:木村太郎:0'
        addressee.append(tmp)
        tmp = '2:baijyaku:810000000000:中村梅雀:0'
        addressee.append(tmp)
        #print addressee

        tw = twiliomanage()
        eventid = tw.geteventid()
        status = define.EVENT_STATUS['WAITING']
        lastnum = 0
        tw.eventregister(eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum)
        for record in addressee:
            print record
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

        db = sqlitedb()
        eventrec = db.getactiveevent()
        for event in eventrec:
            print event['eventid']
            tw = twiliomanage()
            result = tw.callrequest(event['eventid'])

if __name__ == '__main__':

    argvs = sys.argv
    argc = len(argvs)
    if (argc != 2):
        print 'Usage: You should specify 1 parameter'
    main(argvs[1])
