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
        #evinfo = db.geteventinfo(eventid)
        #evinfo_status = evinfo[1] 
        #evinfo_testflg = evinfo[2]
        #evinfo_hostname = evinfo[3]
        #evinfo_operator = evinfo[4]
        #evinfo_calltype = evinfo[5]
        #evinfo_frequency = evinfo[6]
        #evinfo_language = evinfo[7]
        #evinfo_message = evinfo[8]
        #evinfo_headid = evinfo[9]
        #evinfo_footid = evinfo[10]
        #evinfo_lastnum = evinfo[11]
        dbinfos = db.getactivecall(eventid)
        print 'dbinfos %s' % dbinfos
        tw = twiliomanage()
        for dbinfo in dbinfos:
            #dbinfo_eventid = dbinfo[0]
            #dbinfo_numorder = dbinfo[1]
            #dbinfo_ghid = dbinfo[2]
            #dbinfo_name = dbinfo[3]
            #dbinfo_telno = dbinfo[4]
            #dbinfo_sleep = dbinfo[5]
            #dbinfo_callid = dbinfo[6]
            #dbinfo_attempt = dbinfo[7]
            #dbinfo_latesttime = dbinfo[8]
            #dbinfo_lateststatus = dbinfo[9]
            #print 'eventid=%s, numorder=%s, ghid=%s, name=%s, telno=%s, sleep=%s, callid=%s, attempt=%s, latesttime=%s, lateststatus=%s' % (dbinfo[0],dbinfo[1],dbinfo[2],dbinfo[3],dbinfo[4],dbinfo[5],dbinfo[6],dbinfo[7],dbinfo[8],dbinfo[9])
            #result = tw.call(dbinfo_ghid, dbinfo_name, dbinfo_telno, evinfo_testflg, evinfo_hostname, evinfo_message, evinfo_headid, evinfo_footid) 
            result = tw.call('ichiro', 'suzuki', '0000', '1', 'hoge.example.com', 'message is hoge', '1', '1')
