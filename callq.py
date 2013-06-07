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
        twilio = twiliomanage()
        result = twilio.callrequest(eventid)
