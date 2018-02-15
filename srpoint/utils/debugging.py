"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from time import time
#from functools import wraps
from srpoint.settings import PROFILING_SUSPECT_DURATION, PROFILING
from srpoint.utils.logging import logger


def timetrace(func):
	if PROFILING:
		def wrapper(*args, **kwds):
			try:
				start = time()
				return func(*args, **kwds)
			finally:
				elapsed = time() - start
				if elapsed >= PROFILING_SUSPECT_DURATION:
					logger.warning("Duration trace: {}.{} took  {} seconds to finish".format(func.__module__, func.__name__, elapsed))
				else:
					logger.debug("Duration trace: {}.{} took  {} seconds to finish".format(func.__module__, func.__name__, elapsed))
		return wrapper
	else:
		def wrapper(*args, **kwds):
			return func(*args, **kwds)
		return wrapper
