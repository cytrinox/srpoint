"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import mimetypes
import os
import uuid
from jinja2 import Environment, FileSystemLoader
from lxml.html import fromstring as lxml_fromstring, tostring as lxml_tostring


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

jinja2_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


class Message(object):
	def __init__(self, data, template, lang='en'):
		self.template = template
		self.vars = data
		self.lang = lang
		self.attachments = []
		self.charset = 'utf-8'

	def attach_file(self, file, filename=None, mime=None, cid=None):
		assert(file)
		if not mime:
			mime, encoding = mimetypes.guess_type(file)
			if mime is None:
				mime = 'application/octet-stream'
		maintype, subtype = mime.split('/', 1)
		if not filename:
			filename = os.path.basename(file)
		attm = {
			'filename': filename,
			'path': file,
			'maintype': maintype,
			'subtype': subtype,
			'content': None,
			'cid': cid,
		}
		with open(file, 'rb') as fp:
			attm['content'] = fp.read()
		self.attachments.append(attm)

	def render(self, mode, context):
		tmpl = self.template_name(mode, self.lang)
		if os.path.exists(os.path.join(TEMPLATE_DIR, tmpl)):
			return jinja2_env.get_template(tmpl).render(context)
		else:
			tmpl = self.template_name(mode)
			return jinja2_env.get_template(tmpl).render(context)

	def template_dir(self):
		return os.path.join(os.path.dirname(__file__), 'templates')

	def template_name(self, mode, lang=None):
		if lang:
			return "{0}/{0}.{2}.tmpl.{1}".format(self.template, mode, lang)
		else:
			return "{0}/{0}.tmpl.{1}".format(self.template, mode)

	def to_text(self):
		return self.render(mode='txt', context=self.vars)

	def to_html(self):
		html = self.render(mode='html', context=self.vars)
		tree = lxml_fromstring(html)
		for img in filter(lambda x: x.attrib['src'], tree.iter('img')):
			src = os.path.join(self.template_dir(), img.attrib['src'])
			if os.path.exists(src):  # check if local file
				if not any(a['path'] == src and a['cid'] for a in self.attachments):
					self.attach_file(src, cid=str(uuid.uuid4()))
				cid = [a['cid'] for a in self.attachments if a['path'] == src and a['cid']][0]
				src = "cid:{}".format(cid)
				img.attrib['src'] = src
		return lxml_tostring(tree, pretty_print=True, encoding="unicode", method='html')

	def to_telegram(self):
		return self.render(mode='md', context=self.vars)

	def to_email(self):
		body = MIMEMultipart('mixed')
		content = MIMEMultipart('alternative')
		mime_text = MIMEText(self.to_text(), 'plain', self.charset)
		mime_html = MIMEText(self.to_html(), 'html', self.charset)
		mime_related = MIMEMultipart('related')
		map(lambda part: part.add_header('Content-Disposition', 'inline'), [mime_text, mime_html])
		content.attach(mime_text)
		mime_related.attach(mime_html)
		content.attach(mime_related)
		body.attach(content)
		for attm in self.attachments:
			if attm['maintype'] == 'text':
				msg = MIMEText(attm['content'], _subtype=attm['subtype'])
			elif attm['maintype'] == 'image':
				msg = MIMEImage(attm['content'], _subtype=attm['subtype'])
			elif attm['maintype'] == 'audio':
				msg = MIMEAudio(attm['content'], _subtype=attm['subtype'])
			else:
				msg = MIMEBase(attm['maintype'], attm['subtype'])
				msg.set_payload(attm['content'])
				encoders.encode_base64(msg)
			if attm['cid']:
				msg.add_header('Content-ID', '<{}>'.format(attm['cid']))
				msg.add_header('Content-Disposition', 'inline')
			else:
				msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attm['filename']))
			if attm['cid']:  # add to html part
				mime_related.attach(msg)
			else:
				body.attach(msg)  # add to mixed part
		return body
