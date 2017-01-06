"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from .errors import ModelException
from email_validator import validate_email, EmailNotValidError
from uuid import UUID
from srpoint.settings import DEBUG


def must_have(obj, attr):
	if attr not in obj:
		raise ModelException("Instance of {} must have an attribute {}".format(obj.__class__.__name__, attr))


def must_have_value(obj, attr):
	if attr not in obj or obj[attr] is None:
		raise ModelException("Instance of {} must have a value for attribute {}".format(obj.__class__.__name__, attr))


def valid_guid(id):
	try:
		val = UUID(id, version=4)
		assert(val is not None)
	except ValueError:
		raise ModelException("The value {} is no valid GUID".format(id))


def valid_email(email):
	try:
		v = validate_email(email, check_deliverability=not DEBUG)
		assert(v is not None)
		#email = v["email"]
	except EmailNotValidError as e:
		# email is not valid, exception message is human-readable
		raise ModelException('E-Mail address "{}" is not valid: {}'.format(email, str(e)))


class check(object):

	def __init__(self, cls, **kwargs):
		self.cls = cls
		self.kwargs = kwargs

	def __call__(self, f):
		def wrapped_f(*args):
			items = [x for x in args if isinstance(x, self.cls)]
			if len(items):
				for x in items:
					x.validate(**self.kwargs)
			else:
				raise ModelException("CHECK FAILED: No arguments of type {} to check".format(self.cls))
			#print(args[self.arg])
			return f(*args)
		return wrapped_f
