# -*- coding: utf-8 -*-
import time
import sqlite3
from dbmanage import sqlitedb
from twiliomanage import twiliomanage
import define

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

        #update status of eventdb

        if evinfo_calltype == int(define.CALL_TYPE['paralell']):
            print 'paralell'
            tw = twiliomanage()
            for dbinfo in dbinfos:
                if dbinfo['lateststatus'] == int(define.CALL_STATUS['WAITING']):
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
                    #update lastnum of eventdb
                    #update attempt of calldb
                    print 'debug tw.call'
                    result = tw.call(dbinfo_eventid, dbinfo_numorder, dbinfo_ghid, dbinfo_name, dbinfo_telno, evinfo_testflg, evinfo_hostname, evinfo_message, evinfo_headid, evinfo_footid) 
                    #update lateststatus,latesttime,callid of calldb
        else:
            print 'sequential'
