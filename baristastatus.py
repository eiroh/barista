#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

EVENT_STATUS = {
    'WAITING':'0',
    'IN_PROGRESS':'1',
    'FINISHED':'2',
    'UNKNOWN_ERROR':'99'
}

CALL_STATUS = {
    'WAITING':'0',
    'PREPROCESSING':'1',
    'IN_PROGRESS':'2',
    'FINISHED':'3',
    'UNKNOWN_ERROR':'99'
}

ANSWER_STATUS = {
    'NORESPONSE':'1',
    'POSITIVE':'2',
    'NEGATIVE':'3',
    'UNKNOWN_ERROR':'99'
}

ERROR_CODE = {
    'A':'1',
    'B':'2',
    'C':'3',
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
