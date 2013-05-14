# -*- coding: utf-8 -*-

import time
import sqlite3
from dbmanage import sqlitedb
from twiliomanage import twiliomanage

class callQ(object):
    queue = "baristaCall"
    @staticmethod
    def perform(eventid):
        print 'callQ eventid=%s' % eventid
        db = sqlitedb()
        dbinfos = db.getactivecall(eventid)
        print 'dbinfos %s' % dbinfos
        tw = twiliomanage()
        for dbinfo in dbinfos:
            print dbinfo[0]
            #result = tw.call(dbinfo[0], dbinfo[1], telno, testflg, hostname, message, headid, footid)
            result = tw.call('ichiro', 'suzuki', '0000', '1', 'hoge.example.com', 'message is hoge', '1', '1')
