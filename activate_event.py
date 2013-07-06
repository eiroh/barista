# -*- coding: utf-8 -*-

import time
import sqlite3
from dbmanage import sqlitedb
from pyres import ResQ
from callq import callQ
import ConfigParser
from twiliomanage import twiliomanage

conf = ConfigParser.SafeConfigParser()
conf.read('settings.ini')
resqserver = conf.get('ResQ', 'server')
resqport = conf.get('ResQ', 'port')

db = sqlitedb()
eventrec = db.getactiveevent()
for event in eventrec:
    print event['eventid']
    tw = twiliomanage()
    result = tw.callrequest(event['eventid'])
