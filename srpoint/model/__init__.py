"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import srpoint.settings



if srpoint.settings.DB_ENGINE == 'rethinkdb':
	print("loading rehtinkdb")
	from .redb.users_model import *
else:
	print("loading sqlite")
