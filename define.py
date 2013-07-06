#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

EVENT_STATUS = {
    'WAITING':'0',
    'IN_PROGRESS':'1',
    'FINISHED':'2',
    'UNKNOWN_ERROR':'99'
}

ANSWER_STATUS = {
    'POSITIVE':'1',
    'NEGATIVE':'2',
    'NORESPONSE':'3',
    'UNKNOWN_ERROR':'99'
}

ERROR_CODE = {
    'parameters':'1',
    'connection':'2',
    'UNKNOWN_ERROR':'99'
}

DEBUG_FLG = {
    'off':'0',
    'on':'1'
}

INITIAL_VALUE = {
    'callsid':'1234567890'
}

PUSHED_DIGITS = {
    'positive':'1',
    'negative':'2'
}

CALL_TYPE = {
    'sequential':'1',
    'paralell':'2'
}

MAX_NUM_OF_CALL = 10
MAX_NUM_OF_ADDRESSEE = 100
MAX_SEC_OF_SLEEP = 1800
