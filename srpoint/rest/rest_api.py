"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import falcon

from srpoint import settings
from srpoint.middleware import json, https, headers, handle_404, auth

from .r0.endpoints import init_api_r0
from .dummy import DummyEndpoint


def create_rest_api():
	# Main FALCON app
	api = falcon.API(
		media_type='application/json; charset=utf-8',
		middleware=[
			json.RequireJSON(),
			json.JSONTranslator(),
			https.RequireHTTPS(),
			auth.RequireAuth(),
			headers.BaseHeaders(),
			handle_404.WrongURL()
		]
	)
	init_api_r0(api)
	if settings.DEBUG:
		api.add_route('/ping', DummyEndpoint())
	return api
