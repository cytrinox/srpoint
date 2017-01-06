"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import smtplib
import time

from email.header import make_header


class Mailer(object):
	def __init__(self, host='', port=0, username=None, password=None, use_tls=True):
		self.smtp_host = host
		self.smtp_port = port
		self.smtp_user = username
		self.smtp_password = password
		self.smtp_use_tls = use_tls

	def send(self, message, subject, email_to, email_from=None, email_cc=None, email_bcc=None):
		msg = message.to_email()
		msg['Subject'] = str(make_header([(subject, message.charset)]))
		msg['From'] = email_from
		msg['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.gmtime())
		if email_to:
			if isinstance(email_to, str):
				msg['To'] = email_to
			else:
				msg['To'] = ", ".join(email_to)
		if email_cc:
			if isinstance(email_cc, str):
				msg['Cc'] = email_cc
			else:
				msg['Cc'] = ", ".join(email_cc)
		if email_bcc:
			if isinstance(email_bcc, str):
				msg['Bcc'] = email_bcc
			else:
				msg['Bcc'] = ", ".join(email_bcc)
		server = smtplib.SMTP(host=self.smtp_host)
		if self.smtp_use_tls:
			server.ehlo()
			server.starttls()
			server.ehlo()
		if self.smtp_user:
			server.login(self.smtp_user, self.smtp_password)
		server.send_message(msg)
		server.quit()
