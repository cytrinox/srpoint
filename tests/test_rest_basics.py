"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from .fixtures import AppFixture
from srpoint import settings
import falcon

class TestBasicServer(AppFixture):

	def test_selftest(self):
		self.assertEqual('test'.upper(), 'TEST')

	def test_get_server_status(self):
		doc = {'status': 'ok'}
		result = self.simulate_get('/v1/server_status')
		self.assertEqual(result.status, falcon.HTTP_OK)
		self.assertEqual(result.json, doc)

	def test_basic_headers(self):
		result = self.simulate_get('/v1/server_status')
		self.assertEqual(len(result.cookies), 0)
		self.assertEqual(result.headers['Server'], settings.SERVER_NAME)
