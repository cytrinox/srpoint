"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError, ReqlUserError
#import os
#import sys
#from contextlib import contextmanager

from srpoint.model.detail.user_detail import UserDetail
from srpoint.model.helpers import *
from srpoint.model.errors import ModelException
from srpoint.utils.logging import logger

from .database import *


class UsersModel(DatabaseModel):

	@check(UserDetail, bypass=['id'])
	def create_user(self, data):
		result = None
		username = data['username']
		email = data['email']
		del data['id']  # RethinkDB inserts a new ID
		with self.connection() as db:
			try:
				result = r.do(
					r.branch(username, r.table('users_username_unique').get(username), False),
					r.branch(email, r.table('users_email_unique').get(email), False), (
						lambda user_exists, email_exists:
							r.branch(
								user_exists,
								r.error("User {} already exists in system".format(username)),
								email_exists,
								r.error("E-Mail {} already exists in system".format(email)),
								(
									r.branch(email, r.table('users_email_unique').insert({'email': email}), None),
									r.branch(username, r.table('users_username_unique').insert({'username': username}), None),
									r.table('users').insert(data),
								)
							)
					)
				).run(db)
			except ReqlUserError as e:
				logger.warn("Unable to create new user <{}>, exception was: {}".format(email, str(e)))
				raise ModelException("Unable to create user: username <{}> or email <{}> already exists".format(username, email))
		#if tuple(_['inserted'] for _ in result) == (1, 1, 1):
		if len(result) and "generated_keys" in result[-1]:
			# 3 rows inserted, return new id
			logger.info("Created new user: <{}>".format(email))
			return self.get_user(result[-1]['generated_keys'][0])
		else:  # pragma: no cover
			logger.warn("Unable to create new user <{}>, response was: {}".format(email, result))
			raise ModelException("Insert failed, server response was: {}".format(result))

	def delete_user(self, id):
		pass

	def truncate(self):
		with self.connection() as db:
			r.table('users').delete().run(db)
			r.table('users_email_unique').delete().run(db)
			r.table('users_username_unique').delete().run(db)
		#logger.warn("Truncated users table")

	def get_user(self, id=None, search=None):
		assert(id is not None or search is not None)
		result = None
		with self.connection() as db:
			if id is not None:
				result = r.table('users').get_all(id, index='id').run(db)
			else:
				result = r.table('users').get_all(search, index="search").run(db)
		result = list(result)
		if len(result) == 1:
			return UserDetail(result[0])
		elif len(result) > 1:  # pragma: no cover
			raise ModelException("Duplicate record found?!")
		else:
			return None
			#raise ModelException("User {} / ID {} not found".format(search, id))

	def update_user(self, id, data):
		pass

	def change_password(self, id, new_password):
		pass

	def disable_user(self, id):
		pass

	def enable_user(self, id):
		pass
