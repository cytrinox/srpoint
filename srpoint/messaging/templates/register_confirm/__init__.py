"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from srpoint.messaging.message import Message


class RegisterConfirmMessage(Message):

	def __init__(self, data):
		super().__init__(data, __package__.split('.')[-1])

		self.vars['headline'] = "Please confirm your address"

		#wd = os.path.dirname(__file__)
		#self.attach_file(os.path.join(self.template_dir(), 'assets', 'file.pdf'), filename="agb.pdf")
