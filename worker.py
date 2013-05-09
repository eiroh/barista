# -*- coding: utf-8 -*-

from pyres import setup_logging
from pyres.worker import Worker
from eventq import eventQ
from callq import callQ

setup_logging(procname='ojizosan', log_level='info', filename='/tmp/ojizosan.log')
Worker.run(["ojizosanEvent", "ojizosanCall"])
