"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import logging
import logging.config

from srpoint import settings

logging.config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger("srpoint")
