"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import falcon
import json

from srpoint import settings
from srpoint.utils.token import create_jwt_token, parse_jwt_token
#from srpoint.model.users import UsersModel
from srpoint.model import UsersModel, UserDetail
from srpoint.model.errors import ModelException
from srpoint.utils.logging import logger

class User:
	id = 12345


class SignOn:
	def on_post(self, req, resp):
		email = req.context['doc']['email']
		passwd = req.context['doc']['passwd']

		data = {}
		data['username'] = None
		data['email'] = email
		data['password'] = passwd

		users = UsersModel()

		try:
			user = users.create_user(UserDetail(data))

			assert(isinstance(user, UserDetail))

			token = create_jwt_token(user)

			resp.body = json.dumps({"token": token})
			resp.status = falcon.HTTP_201
		except ModelException as E:
			logger.debug(E)
			raise falcon.HTTPError(falcon.HTTP_CONFLICT,
					title="Conflict",
					description="User already exists")
		except Exception as E:
			logger.debug(E)
			raise falcon.HTTPError(falcon.HTTP_INTERNAL_SERVER_ERROR,
					title="Server Error",
					description="Server Error")



		# users_logged_in = random.randint(0, 1024)  # a more predictable source of information would be better.
		# uwsgi.snmp_set_gauge(40, users_logged_in)


class Auth:
	def on_post(self, req, resp):
		user = req.context['doc']['user']
		passwd = req.context['doc']['passwd']

		if user != passwd:
			pass

		#print(req.auth)

		#print(req.context['doc'])

		token = create_jwt_token(User())

		resp.body = json.dumps({"token": token})
		resp.status = falcon.HTTP_200

		# users_logged_in = random.randint(0, 1024)  # a more predictable source of information would be better.
		# uwsgi.snmp_set_gauge(40, users_logged_in)
