"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import falcon
import json

from srpoint import settings

from srpoint.model.sqlite.users_model import UserModel


class User:
	def on_get(self, req, resp, id):

		if id == 'me':
			user_id = req.context['userid']
		else:
			user_id = None

		if user_id:
			user = UserModel(user_id)

			req.context['result'] = user.get()
		else:
			raise falcon.HTTPError(falcon.HTTP_FORBIDDEN,
					title="Forbidden",
					description="You don't have the credentials to access this resource")

		# users_logged_in = random.randint(0, 1024)  # a more predictable source of information would be better.
		# uwsgi.snmp_set_gauge(40, users_logged_in)
