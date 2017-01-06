"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import unittest

from srpoint.model import UserDetail, UsersModel
from srpoint.model.errors import ModelException


template = {
	'username': 'foobar',
	'email': 'test@example.com'
}


class TestModelUsers(unittest.TestCase):

	def test_create_user_valid(self):
		UsersModel().truncate()
		data = {
			'username': 'foobar',
			'email': 'test@example.com'
		}
		user = UserDetail(data)
		user.validate(bypass=['id'])
		user = UsersModel().create_user(user)
		self.assertTrue(user.validate())
		self.assertTrue(user.is_active())

	def test_create_user_duplicate(self):
		UsersModel().truncate()
		user = UserDetail({'username': 'u1', 'email': 'test1@example.com'})
		user = UsersModel().create_user(user)
		with self.assertRaises(ModelException):
			user = UserDetail({'username': 'u1', 'email': 'test1@example.com'})
			user = UsersModel().create_user(user)

	def test_user_silet(self):
		UsersModel().delete_user(None)
		UsersModel().enable_user(None)
		UsersModel().disable_user(None)
		UsersModel().update_user(None, None)
		UsersModel().change_password(None, None)


	def test_create_user_unknown_field(self):
		UsersModel().truncate()
		data = {
			'username': 'foobar',
			'email': 'test@example.com',
			'dbi2ughkjh': None,
		}
		with self.assertLogs(level='WARN') as cm:
			MSG = "Unknown fields ['dbi2ughkjh'] skipped in UserDetail()"
			user = UserDetail(data)
			user.validate(bypass=['id'])
			self.assertTrue(any([True for v in cm.output if MSG in v]))

	def test_create_user_template_check(self):
		UsersModel().truncate()
		data = {
			'username': 'foobar',
			'email': 'test@example.com'
		}
		user = UserDetail(data)
		self.assertTrue(all(k in user for k in UserDetail.template))

	def test_user_detail(self):
		UsersModel().truncate()
		data = {
			'username': 'foobar',
			'email': 'test@example.com'
		}
		user = UserDetail(data)
		user.validate(bypass=['id'])

	def test_user_validation_email(self):
		UsersModel().truncate()
		data = dict(template)
		del data['email']
		with self.assertRaises(ModelException):
			UserDetail(data).validate(bypass=['id'])

	def test_model_users(self):
		UsersModel().truncate()
		um = UsersModel()
		um.get_user(search='test@test.de')
