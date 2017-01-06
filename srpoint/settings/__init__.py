"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import os

DEBUG = bool(int(os.getenv('SRPOINT_IS_DEBUG', True)))
STAGING = bool(int(os.getenv('SRPOINT_IS_DEBUG', False)))

__version__ = '1'
__codename__ = 'Spring'
__status__ = 'alpha'
__docs__ = 'http://docs.stackres.org'

DEBUG = True

if DEBUG and not STAGING:
	from .development import *
elif STAGING:
	from .staging import *
elif not DEBUG and not STAGING:
	from .production import *
