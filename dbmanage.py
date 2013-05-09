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

define('dbpath', default='./db', help='sqlite db path')

class sqlitedb():
    #def __init__(self):
    #    print 'sqlitedb __init__'

    def _dbmanager(self, query):
        path = options.dbpath
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
        query = ''' create table event (eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid, lastnum) ''';
        self._dbmanager(query)
        query = ''' create table call (eventid, numorder, ghid, name, telno, callid, attempt, latesttime, lateststatus) ''';
        self._dbmanager(query)
        return 'OK'

    def geteventid(self):
        millis = int(round(time.time() * 1000))
        logging.info(millis)
        return millis
 
    def eventregister(self, eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid, lastnum):
        query = ''' insert into event (eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid, lastnum) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ''' %(eventid, status, testflg, hostname, operator, calltype, frequency, message, headid, footid, lastnum);
        self._dbmanager(query)
        return 'OK'

    def callregister(self, eventid, numorder, ghid, name, telno, callid, attempt, latesttime, lateststatus):
        query = ''' insert into call (eventid, numorder, ghid, name, telno, callid, attempt, latesttime, lateststatus) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ''' %(eventid, numorder, ghid, name, telno, callid, attempt, latesttime, lateststatus); 
        self._dbmanager(query)
        return 'OK'

    def getactiveevent(self):
        query = ''' select eventid from event where status != 9''';
        result = self._dbmanager(query)
        return result
