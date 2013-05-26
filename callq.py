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
        evinfo_status = info['status'] 
        evinfo_testflg = info['testflg']
        evinfo_hostname = info['hostname'].encode('utf-8')
        evinfo_operator = info['operator'].encode('utf-8')
        evinfo_calltype = info['calltype']
        evinfo_frequency = info['frequency']
        evinfo_language = info['language'].encode('utf-8')
        evinfo_message = info['message'].encode('utf-8')
        evinfo_headid = info['headid']
        evinfo_footid = info['footid']
        evinfo_lastnum = info['lastnum']
        dbinfos = db.getactivecall(eventid)
        #print 'dbinfos %s' % dbinfos
        tw = twiliomanage()
        for dbinfo in dbinfos:
            dbinfo_eventid = dbinfo['eventid']
            dbinfo_numorder = dbinfo['numorder']
            dbinfo_ghid = dbinfo['ghid'].encode('utf-8')
            dbinfo_name = dbinfo['name'].encode('utf-8')
            dbinfo_telno = dbinfo['telno'].encode('utf-8')
            dbinfo_sleep = dbinfo['sleep']
            dbinfo_callid = dbinfo['callid']
            dbinfo_attempt = dbinfo['attempt']
            dbinfo_latesttime = dbinfo['latesttime'].encode('utf-8')
            dbinfo_lateststatus = dbinfo['lateststatus']
            result = tw.call(dbinfo_eventid, dbinfo_numorder, dbinfo_ghid, dbinfo_name, dbinfo_telno, evinfo_testflg, evinfo_hostname, evinfo_message, evinfo_headid, evinfo_footid) 
            #result = tw.call('ichiro', 'suzuki', '0000', '1', 'hoge.example.com', 'message is hoge', '1', '1')
