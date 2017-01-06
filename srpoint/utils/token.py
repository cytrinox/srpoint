"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from datetime import datetime, timedelta

import jwt
import falcon

from srpoint import settings



def create_jwt_token(user):
	now = datetime.utcnow()
	exp = datetime.utcnow() + timedelta(hours=settings.SESSION_EXPIRES)
	payload = {
		'iss': settings.SITE_DOMAIN,
		'sub': user.id,
		'iat': now,
		'exp': exp
	}
	token = jwt.encode(payload, settings.SECRET)
	return token.decode('unicode_escape')


def parse_jwt_token(auth):
	parts = auth.split()

	if parts[0].lower() != 'bearer':
		raise falcon.HTTPError(falcon.HTTP_401,
							   title="Invalid Header",
							   description="Authorization header must start with Bearer")
	elif len(parts) == 1:
		raise falcon.HTTPError(falcon.HTTP_401,
							   title="Invalid Header",
							   description="Token not found")
	elif len(parts) > 2:
		raise falcon.HTTPError(falcon.HTTP_401,
							   title="Invalid Header",
							   description="Authorization header must be Bearer + \s + token")
	return jwt.decode(parts[1], settings.SECRET)
