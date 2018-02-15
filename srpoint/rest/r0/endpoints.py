"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from .accounts_auth import AccountAuth
from srpoint import settings


SRPOINT_REST_R0_PART = '/srp/r0'

def init_api_r0(api):
	assert(api)
	api.add_route(SRPOINT_REST_R0_PART + '/accounts/auth', AccountAuth())
	return api
