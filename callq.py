# -*- coding: utf-8 -*-

import time
import sqlite3
from dbmanage import sqlitedb

class callQ(object):

    queue = "ojizosanCall"

    @staticmethod
    def perform(eventid):

        print (eventid)
        #db = sqlitedb()
        #eventrec = db.getactiveevent()
        #for event in eventrec:
        #    print event
