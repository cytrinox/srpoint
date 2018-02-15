"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import falcon

from jwt.exceptions import InvalidTokenError

from srpoint import settings
from srpoint.utils.logging import logger
from srpoint.utils.token import parse_jwt_token


class RequireAuth(object):
	"""Force authentication.
	"""
	whitelist = (
		'/ping',
		'/v1/serverstatus',
		'/v1/users',
		'/v1/users/me/login',
	)

	def process_request(self, req, resp):
		if req.path not in self.whitelist:
			if req.auth:
				try:
					payload = parse_jwt_token(req.auth)
					if payload['iss'] != settings.SITE_DOMAIN:

							logger.debug("JWT token expired or malformed")
							raise falcon.HTTPError(falcon.HTTP_401, title="Credentials expired",
								description="Your crendentials have expired. Please login again.")
					else:
						req.context['userid'] = payload['sub']
				except (InvalidTokenError) as E:
					logger.debug(str(E))
					raise falcon.HTTPError(falcon.HTTP_401, title="Credentials expired",
						description="Your crendentials have expired. Please login again.")
			else:
				logger.debug("No JWT token found")
				raise falcon.HTTPError(falcon.HTTP_401,
					title="Credentials not found",
					description="You don't have the credentials to access this resource")
		else:
			pass
