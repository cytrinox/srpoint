"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""


class DatabaseDetail(dict):
	@property
	def id(self):
		return self['id']

	def available_checks(self):
		return set(x[6:] for x in dir(self) if x.startswith('check_'))

	def validate(self, **kwargs):
		run_checks = self.available_checks()
		if 'bypass' in kwargs:
			run_checks = run_checks - set(kwargs['bypass'])
		for chk in run_checks:
			getattr(self, "check_" + chk)()
		return True
