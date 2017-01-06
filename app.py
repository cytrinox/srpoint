"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import sys
import signal

from srpoint import create_api

from srpoint.utils.logging import logger
from srpoint.utils.checks import check_python
#from srpoint import settings

check_python()


def signal_handler_int(signal, frame):
	logger.info("Exiting...")
	sys.exit(0)


signal.signal(signal.SIGINT, signal_handler_int)


# Main FALCON app
api = create_api()


# Sharing
#api.add_route(api_version + '/share', sharing.Share())

logger.debug("API service started")


if __name__ == '__main__':
	from wsgiref import simple_server
	httpd = simple_server.make_server('0.0.0.0', 8000, api)
	httpd.serve_forever()
