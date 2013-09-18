# -*- coding: utf-8 -*-

from pyres import setup_logging
from pyres.worker import Worker
from eventq import eventQ
from callq import callQ

setup_logging(procname='barista', log_level='INFO', filename='/tmp/barista.log')
Worker.run(["baristaEvent", "baristaCall"])
