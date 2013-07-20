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
from barista import barista

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')

def makedata(type):
    calltype = int(define.CALL_TYPE['sequential'])
    if type == 'paralell':
        calltype = int(define.CALL_TYPE['paralell'])
    testflg = int(define.DEBUG_FLG['on'])
    hostname = 'test.example.com'
    operator = 'testuser'
    #calltype = int(define.CALL_TYPE['paralell'])
    #calltype = int(define.CALL_TYPE['sequential'])
    frequency = 3
    language = 'ja-jp'
    message = 'Socket timeout after 10 secondsです'
    headid = 1
    footid = 1

    addressee = []
    tmp = '1:tarou:810000000000:木村太郎:120'
    addressee.append(tmp)
    tmp = '2:baijyaku:810000000000:中村梅雀:120'
    addressee.append(tmp)
    tmp = '3:kouji:810000000000:加藤浩二:120'
    addressee.append(tmp)

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
    print 'eventid = %s' % eventid

def activate():
    activate_events()
    return

def updatestatus():
    db = sqlitedb()
    db.updatelateststatusfortest('baijyaku',1)
    return

def updatetime():
    db = sqlitedb()
    db.updatelatesttimefortest('tarou')
    db.updatelatesttimefortest('baijyaku')
    db.updatelatesttimefortest('kouji')
    return

def activate_events():
    db = sqlitedb()
    eventrec = db.getactiveevent()
    for event in eventrec:
        print 'activate_events:found active events %s' % event['eventid']
        tw = twiliomanage()
        result = tw.callrequest(event['eventid'])
    return

def getlog():
    db = sqlitedb()
    eventids = db.gettestevent()
    #print eventids
    main = barista()
    result = main.getLog(eventids[0]['eventid'])
    print result.encode('utf-8')

if __name__ == '__main__':

    argvs = sys.argv
    argc = len(argvs)
    tw = twiliomanage()
    tw.initdb()
    if argvs[1] == 'makedata':
        if (argc == 3):
            if argvs[2] == 'sequential' or argvs[2] == 'paralell':
                makedata(argvs[2])
            else:
                print 'specify sequential/paralell as 2nd parameter'
        else:
            print 'needs 2 parameteres'
    elif argvs[1] == 'activate':
        activate()
    elif argvs[1] == 'updatestatus':
        updatestatus()
    elif argvs[1] == 'updatetime':
        updatetime()
    elif argvs[1] == 'getlog':
        getlog()
    else:
        print 'unknown method'
