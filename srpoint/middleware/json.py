"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import json
import falcon
import datetime
import decimal
import uuid

from srpoint import settings


class RequireJSON(object):

	def process_request(self, req, resp):
		if not req.client_accepts_json:
			raise falcon.HTTPNotAcceptable(
				'This API only supports responses encoded as JSON.',
				href=settings.__docs__)

		if req.method in ('POST', 'PUT'):
			if 'application/json' not in req.content_type:
				raise falcon.HTTPUnsupportedMediaType(
					'This API only supports requests encoded as JSON.',
					href=settings.__docs__)


class JSONTranslator(object):
	@staticmethod
	def alchemyencoder(obj):
		"""JSON encoder function for SQLAlchemy special classes."""
		if isinstance(obj, datetime.date):
			return obj.isoformat()
		elif isinstance(obj, decimal.Decimal):
			return float(obj)
		elif isinstance(obj, uuid.UUID):
			return str(obj)

	def process_request(self, req, resp):
		# req.stream corresponds to the WSGI wsgi.input environ variable,
		# and allows you to read bytes from the request body.
		#
		# See also: PEP 3333
		if req.content_length in (None, 0):
			# Nothing to do
			return

		body = req.stream.read()
		if not body:
			raise falcon.HTTPBadRequest('Empty request body',
										'A valid JSON document is required.')

		try:
			req.context['doc'] = json.loads(body.decode('utf-8'))

		except (ValueError, UnicodeDecodeError):
			raise falcon.HTTPError(falcon.HTTP_753,
								   'Malformed JSON',
								   'Could not decode the request body. The '
								   'JSON was incorrect or not encoded as '
								   'UTF-8.')

	def process_response(self, req, resp, resource):
		if 'result' not in req.context:
			return

		resp.body = json.dumps(
			req.context['result'], default=JSONTranslator.alchemyencoder)
