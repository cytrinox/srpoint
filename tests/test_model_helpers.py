"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import unittest

from srpoint.model.helpers import *
from srpoint.model.detail import DatabaseDetail
from srpoint.model.errors import ModelException
from uuid import uuid4
from ddt import ddt, data as testdata, file_data, unpack


class SampleDetail(DatabaseDetail):
	def check_foo(self):
		pass


@ddt
class TestModelHelpers(unittest.TestCase):

	def test_must_have(self):
		data = {'x': None}
		must_have(data, 'x')

	def test_must_have_fail(self):
		data = {'x': None}
		with self.assertRaises(ModelException):
			must_have(data, 'y')

	def test_must_have_value(self):
		data = {'x': 5}
		must_have_value(data, 'x')

	def test_must_have_value_fail(self):
		data = {'x': None}
		with self.assertRaises(ModelException):
			must_have_value(data, 'x')

	@file_data("valid_emails.json")
	def test_valid_email(self, email):
		valid_email(email)

	@file_data("invalid_emails.json")
	def test_valid_email_fail(self, email):
		with self.assertRaises(ModelException):
			valid_email(email)

	def test_valid_guid(self):
		data = str(uuid4())
		valid_guid(data)

	def test_valid_guid_fail(self):
		data = '2867-1112'
		with self.assertRaises(ModelException):
			valid_guid(data)

	def test_check_decorator(self):
		@check(SampleDetail)
		def internal(a, b, c):
			pass
		internal(1, 2, SampleDetail())
		with self.assertRaises(ModelException):
			internal(1, 2, 3)
