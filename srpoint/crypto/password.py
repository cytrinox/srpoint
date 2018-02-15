"""
	SRPOINT - StackRes Point Service
	Copyright (C) 2017  Daniel Vogelbacher <daniel@vogelbacher.name>

	Licensed under AGPL-V3.0, see LICENSE file for more information.
"""

import bcrypt


def hash_password(plain_text_password):
	hash = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(12))
	return hash, None, "bcrypt"

def verify_password(plain_text_password, hashed_password):
    # Check hased password. Useing bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)	
