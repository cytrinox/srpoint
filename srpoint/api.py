"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

#import sys
import falcon

from srpoint.middleware import json, https, headers, handle_404, auth

from srpoint.resources import tests as tests
from srpoint.resources.v1 import auth as v1_auth
from srpoint.resources.v1 import user as v1_user
from srpoint.resources.v1 import server_status as v1_server_status

from srpoint import settings


def create_api():

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

	# URLs
	#api_version = '/app/' + settings.DEFAULT_API
	#api.add_route(api_version, main.APIInfo())
	#api.add_route(api_version + '/accounts', app_v1_account.Accounts())
	#api.add_route(api_version + '/account', app_v1_account.DetailAccount())


	api.add_route('/v1/signon', v1_auth.SignOn())
	api.add_route('/v1/auth', v1_auth.Auth())
	api.add_route('/v1/users/{id}', v1_user.User())


	#api.add_route('/v1/users', v1_user.Users())
	#api.add_route('/v1/users/{id}', v1_user.User())
	#api.add_route('/v1/users/{id}/keys', v1_user.UserKeys())
	#api.add_route('/v1/users/{id}/keys/{id}', v1_user.UserKey())


#api.add_route('/v1/sync/resources', 			v1_sync_resource.Resources())
#api.add_route('/v1/sync/resource/{res_id}', 	v1_sync_resource.DetailResource())


# Public resource sharing
# TODO: Limited sharing
#api.add_route('/v1/pub/resource/{rnd}.{res_id}.{key_id}', v1_pub.Resource())
#api.add_route('/v1/pub/resource/decrypt/{rnd}.{res_id}.{key}', v1_pub.DecryptResource())

# URL Shortening service
#api.add_route('/s/{short_id}', short_url.ShortURL())

	api.add_route('/v1/server_status', v1_server_status.ServerStatus())

	if settings.DEBUG:
		api.add_route('/test_api', tests.TestResource())

	return api
