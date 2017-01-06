"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import json
import falcon

from srpoint import settings


class WrongURL(object):

	def process_response(self, req, resp, resource=''):
		"""Intercept main 404 response by Falcon"""
		if resp.status == falcon.HTTP_404:
			resp.body = json.dumps({"message": "Resource not found",
											"documentation": settings.__docs__})
