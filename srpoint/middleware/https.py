"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import falcon

from srpoint import settings


class RequireHTTPS(object):
	"""Force the connection to be HTTPS.
	"""

	def process_request(self, req, resp):
		if req.protocol == "http" and not settings.DEBUG:
			raise falcon.HTTPBadRequest(title="Client error. HTTP Not Allowed",
										description="API connections over HTTPS only.",
										href=settings.__docs__)
