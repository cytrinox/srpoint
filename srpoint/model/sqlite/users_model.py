"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

from .database import *
import uuid
import apsw


class UserModel(DatabaseModel):

	def __init__(self, id):
		self.data = {'id': id, 'mail': '@mail'}
		with self.connection() as db:
			cursor = db.cursor()
			self.data = cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()

	def get(self):
		return self.data

	@property
	def id(self):
		return self.data['id']


class UsersModel(DatabaseModel):
	def create(self, data):
		with self.connection() as db:
			cursor = db.cursor()
			id = str(uuid.uuid4())

			self.data = cursor.execute("INSERT INTO users(id, email, username) VALUES(:id, :email, :username)",
				{'id': id,
				'email': data['email'], 'username': 'blaaa'})

			return UserModel(id)


"""
class ResourceModel(DatabaseModel):
	pass


class ResourcesModel(DatabaseModel):

	def get_list_modified_since(self, last_ts):
		pass

	def get_all(self, newer_than=None, compact=False):
		pass

	def get_by_id(self, id):
		pass

	def update_by_id(self, id, data):
		pass

	def delete_by_id(self, id):
		pass

	def share_by_id(self, id, userid):
		pass

	def unshare_by_id(self, id, userid):
		pass

	def get_meta_by_id(self, id):
		pass

"""

