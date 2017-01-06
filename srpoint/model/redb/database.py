"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import rethinkdb as r
#from rethinkdb.errors import RqlRuntimeError, RqlDriverError, ReqlUserError
import os
#import sys
from contextlib import contextmanager

#from srpoint.model.detail.user_detail import UserDetail
#from srpoint.model.helpers import *

RDB_HOST = os.environ.get('RDB_HOST') or 'localhost'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
RDB_DB = 'srpoint'


class RethinkdbUnpooledMixin:
	@contextmanager
	def connection(self):
		db = r.connect(host=RDB_HOST, port=RDB_PORT, db=RDB_DB)
		yield db
		db.close()


class DatabaseModel(RethinkdbUnpooledMixin, object):
	pass
