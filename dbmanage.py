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
import ConfigParser
import define

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
options_dbpath = conf.get('SQLite', 'dbpath')

class sqlitedb():

    def _dbmanager(self, query):
        path = options_dbpath
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        cursorobj = connection.cursor()
        try:
            cursorobj.execute(query)
            result = cursorobj.fetchall()
            connection.commit()
        except Exception:
            raise
        connection.close()
        return result

    def initdb(self):
        result = os.path.exists(options_dbpath)
        #print 'initdb %s' % result
        if result == False:
            query = ''' create table event (eventid INTEGER, status INTEGER, testflg INTEGER, hostname TEXT, operator TEXT, calltype INTEGER, frequency INTEGER, language TEXT, message TEXT, headid INTEGER, footid INTEGER, lastnum INTEGER) ''';
            self._dbmanager(query)
            query = ''' create table call (eventid INTEGER, numorder INTEGER, ghid TEXT, name TEXT, telno TEXT, sleep INTEGER, callid INTEGER, attempt INTEGER, latesttime TEXT, lateststatus INTEGER) ''';
            self._dbmanager(query)
            return

    def geteventid(self):
        millis = int(round(time.time() * 1000))
        logging.info(millis)
        return millis
 
    def eventregister(self, eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum):
        query = ''' insert into event (eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ''' %(eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum);
        self._dbmanager(query)
        return

    def callregister(self, eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus):
        query = ''' insert into call (eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ''' %(eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus); 
        self._dbmanager(query)
        return

    def updateattempt(self, eventid, numorder, ghid):
        print 'updateattempt: eventid=%s,numorder=%s,ghid=%s' % (eventid, numorder, ghid)
        query = ''' update call set attempt = attempt + 1 where eventid='%s' and numorder='%s' and ghid='%s' ''' %(eventid, numorder, ghid);
        self._dbmanager(query)
        query = ''' update event set lastnum ='%s' where eventid='%s' ''' %(numorder, eventid);
        self._dbmanager(query)
        return

    def insertsid(self, eventid, numorder, ghid, sid):
        print 'insertsid: eventid=%s,numorder=%s,ghid=%s,sid=%s' % (eventid, numorder, ghid, sid)
        millis = int(round(time.time() * 1000))
        query = ''' update call set callid='%s', latesttime ='%s' where eventid='%s' and numorder='%s' and ghid='%s' ''' %(sid, millis, eventid, numorder, ghid);
        self._dbmanager(query)
        return

    def getactiveevent(self):
        query = ''' select eventid from event where (status = %s) ''' %(define.EVENT_STATUS['WAITING']);
        result = self._dbmanager(query)
        return result

    def getactivecall(self, eventid, frequency):
        query = ''' select * from call where eventid == '%s' and (lateststatus == '%s' or lateststatus == '%s') and (attempt < '%s') order by attempt, numorder ''' %(eventid, define.ANSWER_STATUS['NORESPONSE'], define.ANSWER_STATUS['UNKNOWN_ERROR'], frequency);
        result = self._dbmanager(query)
        return result

    def updatelateststatus(self, callsid, lateststatus):
        millis = int(round(time.time() * 1000))
        query = ''' update call set latesttime ='%s', lateststatus ='%s' where callid='%s' ''' %(millis, lateststatus, callsid);
        result = self._dbmanager(query)
        return result

    def updatelateststatusfortest(self, ghid, lateststatus):
        millis = int(round(time.time() * 1000))
        query = ''' update call set latesttime ='%s', lateststatus ='%s' where ghid='%s' ''' %(millis, lateststatus, ghid);
        result = self._dbmanager(query)
        return result

    def geteventinfo(self, eventid):
        query = ''' select * from event where eventid = '%s' ''' %(eventid);
        result = self._dbmanager(query)
        return result

    def finishevent(self, eventinfo):
        query = ''' update event set status ='%s' where eventid='%s' ''' %(define.EVENT_STATUS['FINISHED'], eventinfo['eventid']);
        self._dbmanager(query)
        return 

    def startevent(self, eventinfo):
        query = ''' update event set status ='%s' where eventid='%s' ''' %(define.EVENT_STATUS['IN_PROGRESS'], eventinfo['eventid']);
        self._dbmanager(query)
        return

    def getalllog(self, eventid):
        query = ''' select * from event where eventid = '%s' ''' %(eventid);
        eventresult = self._dbmanager(query)
        query = ''' select * from call where eventid = '%s' order by numorder ''' %(eventid);
        callresult = self._dbmanager(query)
        return dict(event=eventresult,call=callresult)

    def findAnswer(self, eventid):
        query = ''' select * from call where eventid == '%s' and (lateststatus == '%s' or lateststatus == '%s') order by attempt, numorder ''' %(eventid, define.ANSWER_STATUS['POSITIVE'], define.ANSWER_STATUS['NEGATIVE']);
        result = self._dbmanager(query)
        return result

    def gettestevent(self):
        query = ''' select eventid from event where operator = 'testuser' ''';
        result = self._dbmanager(query)
        return result
