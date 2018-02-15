"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import os


# Add the current directory to the python path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Database engine to use, choose rethinkdb or sqlite
DB_ENGINE = 'rethinkdb'

RETHINKDB_CONF = {
	'HOST': 'localhost'
}

SQLITE_CONF = {
	'DATABASE': 'srpoint.db'
}

# Select the default version of the API.
DEFAULT_API = 'v1'

# Site domain, you usually want this to be your frontend url. This is used for
# login verification between other things like CORS
CORS_ACTIVE = True
SITE_DOMAIN = 'https://api.stackres.com'

# This rewrites the response "Server" header, so you can hide your server name
# for protection
SERVER_NAME = "api.stackres.com"

# How long the user session will last (in hours). Default: 168 (7 days)
SESSION_EXPIRES = 168

# Main server token Make it unique and keep it away from strangers! This token
# is used in authentication and part of the storage encryption. This token
# is an example. **You MUST replace it!**
SECRET = '***DUMMY_TOKEN***'

# Profiling settings
# Report functions running for more than 1.5 seconds with INFO level
PROFILING_SUSPECT_DURATION = 1.5
PROFILING = False

# Logging settings. This is a standard python logging configuration. The levels
# are supposed to change depending on the settings file, to avoid clogging the
# logs with useless information.
LOGFILE = 'srpoint.log'
LOG_CONFIG = {
	"version": 1,
	'formatters': {
		'standard': {
			'format': "[%(asctime)s] %(levelname)s [%(filename)s->%(funcName)s:%(lineno)s] %(message)s",
			'datefmt': "%Y/%m/%d %H:%M:%S"
		},
	},
	'handlers': {
		'logfile': {
			'level': 'DEBUG',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': os.path.join(BASE_DIR, LOGFILE),
			'maxBytes': 2097152,  # 2MB per file
			'backupCount': 2,  # Store up to three files
			'formatter': 'standard',
		},
		'stderr': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'standard',
		},
	},
	'loggers': {
		'srpoint': {
			'handlers': ["logfile", "stderr", ],
			#'handlers': ["logfile", ],
			'level': 'DEBUG',
		},
	}
}
