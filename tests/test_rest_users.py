"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from .fixtures import AppFixture, auth_token
#from srpoint import settings
import falcon
import json

from srpoint.model import UsersModel


class TestUsers(AppFixture):

	def setUp(self):
		super().setUp()
		UsersModel().truncate()

	def test_create_user(self):
		doc = {'user': 'foo', 'passwd': 'bar', 'email': 'example@example.com'}
		result = self.simulate_post('/v1/signon', body=json.dumps(doc), headers=[('Content-Type', 'application/json'), ])
		self.assertEqual(result.status, falcon.HTTP_CREATED)
		self.assertIn('token', result.json)

		# check for duplicate
		result = self.simulate_post('/v1/signon', body=json.dumps(doc), headers=[('Content-Type', 'application/json'), ])
		self.assertEqual(result.status, falcon.HTTP_CONFLICT)
		#self.assertEqual(result.json, doc)

	def test_login(self):
		doc = {'user': 'foo', 'passwd': 'bar'}
		result = self.simulate_post('/v1/auth', body=json.dumps(doc), headers=[('Content-Type', 'application/json'), ])
		self.assertEqual(result.status, falcon.HTTP_OK)
		self.assertIn('token', result.json)

	def test_lock_user(self):
		pass

	def test_delete_user(self):
		pass

	def test_user_data_unauth(self):
		result = self.simulate_get('/v1/user/me')
		self.assertEqual(result.status, falcon.HTTP_UNAUTHORIZED)

	def test_user_data_auth(self):
		doc = {'user': 'foo', 'passwd': 'bar'}
		result = self.simulate_post('/v1/auth', body=json.dumps(doc), headers=[('Content-Type', 'application/json'), ])
		self.assertEqual(result.status, falcon.HTTP_OK)
		self.assertIn('token', result.json)

		token = result.json

		result = self.simulate_get('/v1/users/me', headers=[auth_token(token)])
		self.assertEqual(result.status, falcon.HTTP_OK)

		result = self.simulate_get('/v1/users/12345', headers=[auth_token(token)])
		self.assertEqual(result.status, falcon.HTTP_FORBIDDEN)
