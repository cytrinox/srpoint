"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from srpoint import settings
#from srpoint.utils.logging import logger


class BaseHeaders(object):

	def process_response(self, req, res, resource):
		res.set_headers([
			('Cache-Control', 'no-store, must-revalidate, no-cache, max-age=0'),
			('Content-Type', 'application/json; charset=utf-8'),
			('Server', settings.SERVER_NAME),
		])
