"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import unittest
import falcon

from jwt.exceptions import DecodeError

from srpoint.utils.token import *


class Dummy(object):
	def __init__(self):
		super().__init__()
		self.id = None


class TestUtilsToken(unittest.TestCase):

	def test_token(self):
		data = Dummy()
		data.id = 1234
		token = create_jwt_token(data)

		result = parse_jwt_token('Bearer ' + token)
		self.assertEqual(result['sub'], 1234)


	def test_token_invalid(self):
		data = Dummy()
		data.id = 1234
		token = create_jwt_token(data)

		with self.assertRaises(falcon.HTTPError):
			parse_jwt_token('Something')

		with self.assertRaises(falcon.HTTPError):
			parse_jwt_token('Bearer')

		with self.assertRaises(falcon.HTTPError):
			parse_jwt_token('Bearer 2 3 4 5')

		with self.assertRaises(DecodeError):
			parse_jwt_token('Bearer ' + token + 'invalid')
