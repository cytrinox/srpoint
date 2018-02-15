"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import falcon
import json

from srpoint import settings


class AccountAuth:
	def on_post(self, req, resp):
		req.context['result'] = {'status': 'ok'}

		# users_logged_in = random.randint(0, 1024)  # a more predictable source of information would be better.
		# uwsgi.snmp_set_gauge(40, users_logged_in)
