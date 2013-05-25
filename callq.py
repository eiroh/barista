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
        evinfo = db.geteventinfo(eventid)
        info = evinfo[0]
        evinfo_status = info[1] 
        evinfo_testflg = info[2]
        evinfo_hostname = info[3].encode('utf-8')
        evinfo_operator = info[4].encode('utf-8')
        evinfo_calltype = info[5]
        evinfo_frequency = info[6]
        evinfo_language = info[7].encode('utf-8')
        evinfo_message = info[8].encode('utf-8')
        evinfo_headid = info[9]
        evinfo_footid = info[10]
        evinfo_lastnum = info[11]
        dbinfos = db.getactivecall(eventid)
        #print 'dbinfos %s' % dbinfos
        tw = twiliomanage()
        for dbinfo in dbinfos:
            dbinfo_eventid = dbinfo[0]
            dbinfo_numorder = dbinfo[1]
            dbinfo_ghid = dbinfo[2].encode('utf-8')
            dbinfo_name = dbinfo[3].encode('utf-8')
            dbinfo_telno = dbinfo[4].encode('utf-8')
            dbinfo_sleep = dbinfo[5]
            dbinfo_callid = dbinfo[6]
            dbinfo_attempt = dbinfo[7]
            dbinfo_latesttime = dbinfo[8].encode('utf-8')
            dbinfo_lateststatus = dbinfo[9]
            result = tw.call(dbinfo_eventid, dbinfo_numorder, dbinfo_ghid, dbinfo_name, dbinfo_telno, evinfo_testflg, evinfo_hostname, evinfo_message, evinfo_headid, evinfo_footid) 
            #result = tw.call('ichiro', 'suzuki', '0000', '1', 'hoge.example.com', 'message is hoge', '1', '1')
