# -*- coding: utf-8 -*-

import time
import sqlite3
from dbmanage import sqlitedb
from pyres import ResQ
from callq import callQ
import ConfigParser

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')

resqserver = conf.get('ResQ', 'server')
resqport = conf.get('ResQ', 'port')

class eventQ(object):

    queue = "ojizosanEvent"

    @staticmethod
    def perform(eventid):

        print (eventid)
        db = sqlitedb()
        eventrec = db.getactiveevent()
        for event in eventrec:
            print event
            r = ResQ(server="%s:%s" % (resqserver, resqport))
            r.enqueue(callQ, event)
