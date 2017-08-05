"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""


import apsw

import os
#import sys
from contextlib import contextmanager


def row_factory(cursor, row):
	columns = [t[0] for t in cursor.getdescription()]
	return dict(zip(columns, row))


class SqliteApswMixin:
	@contextmanager
	def connection(self):
		db = apsw.Connection("point.db")
		db.setrowtrace(row_factory)
		yield db
		db.close()


class DatabaseModel(SqliteApswMixin, object):
	pass
