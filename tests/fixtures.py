"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from falcon import testing
from srpoint.rest.rest_api import create_rest_api


class AppFixture(testing.TestCase):

	def setUp(self):
		super(AppFixture, self).setUp()
		self.app = create_rest_api()


def auth_token(token):
	if isinstance(token, dict):
		return ('Authorization', 'Bearer ' + token['token'])
	else:
		return ('Authorization', 'Bearer ' + token)
