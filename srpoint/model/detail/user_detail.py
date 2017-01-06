"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from srpoint.model.detail import DatabaseDetail
from srpoint.model.helpers import must_have, must_have_value, valid_guid, valid_email
from srpoint.utils.logging import logger


class UserDetail(DatabaseDetail):
	""" Detail for a single USER
	"""

	""" Template for a new USER """
	template = {
		'id': None,
		'email': None,
		'username': None,
		'cts': None,
		'mts': None,
		'enabled': True,
		'verified': False,
		'blocked': False,
		'created_ip': None,
		'created_agent': None,
		'quota_max': 1024*1024*50,  # 50 MiB Quota
	}

	def __init__(self, data):
		# Copy values from template and data
		x = {k: (data[k] if k in data else v) for k, v in UserDetail.template.items()}
		super().__init__(x)
		unused = [k for k in data if k not in UserDetail.template]
		if len(unused):
			logger.warn('Unknown fields {} skipped in UserDetail()'.format(unused))


	def is_active(self):
		return self['enabled'] and not self['blocked']

	def check_required(self):
		must_have_value(self, 'email')
		must_have(self, 'username')

	def check_id(self):
		must_have_value(self, 'id')
		valid_guid(self.id)

	def check_email(self):
		must_have_value(self, 'email')
		valid_email(self['email'])

	def check_range(self):
		return True
