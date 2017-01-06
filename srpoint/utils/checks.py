"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import sys


def check_python():
	if sys.version_info <= (3, 3):
		sys.stdout.write("\nSorry, requires Python 3.3.x or better.\n")
		sys.exit(1)
