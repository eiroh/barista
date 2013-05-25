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

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
options_dbpath = conf.get('MySQL', 'dbpath')

class sqlitedb():

    def _dbmanager(self, query):
        path = options_dbpath
        connection = sqlite3.connect(path)
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
        print 'initdb %s' % result
        if result == False:
            query = ''' create table event (eventid INTEGER, status INTEGER, testflg INTEGER, hostname TEXT, operator TEXT, calltype INTEGER, frequency INTEGER, language TEXT, message TEXT, headid INTEGER, footid INTEGER, lastnum INTEGER) ''';
            self._dbmanager(query)
            query = ''' create table call (eventid INTEGER, numorder INTEGER, ghid TEXT, name TEXT, telno TEXT, sleep INTEGER, callid INTEGER, attempt INTEGER, latesttime TEXT, lateststatus INTEGER) ''';
            self._dbmanager(query)
            return 'OK'

    def geteventid(self):
        millis = int(round(time.time() * 1000))
        logging.info(millis)
        return millis
 
    def eventregister(self, eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum):
        query = ''' insert into event (eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ''' %(eventid, status, testflg, hostname, operator, calltype, frequency, language, message, headid, footid, lastnum);
        self._dbmanager(query)
        return 'OK'

    def callregister(self, eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus):
        query = ''' insert into call (eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ''' %(eventid, numorder, ghid, name, telno, sleep, callid, attempt, latesttime, lateststatus); 
        self._dbmanager(query)
        return 'OK'

    def insertsid(self, eventid, numorder, ghid, sid):
        print 'insertsid: eventid=%s,numorder=%s,ghid=%s,sid=%s' % (eventid, numorder, ghid, sid)
        query = ''' update call set callid='%s', lateststatus='%s' where eventid='%s' and numorder='%s' and ghid='%s' ''' %(sid, '1', eventid, numorder, ghid);
        self._dbmanager(query)
        return 'OK'

    def getactiveevent(self):
        #query = ''' select eventid from event where (status = '1' or status = '2') and testflg = '0' ''';
        query = ''' select eventid from event where (status = '1' or status = '2') ''';
        result = self._dbmanager(query)
        return result

    def getactivecall(self, eventid):
        query = ''' select * from call where eventid == '%s' and (lateststatus == '1' or lateststatus == '2') order by numorder ''' %(eventid);
        result = self._dbmanager(query)
        return result

    def geteventinfo(self, eventid):
        query = ''' select * from event where eventid = '%s' ''' %(eventid);
        result = self._dbmanager(query)
        return result
