import rethinkdb as r
r.connect('localhost', 28015).repl()

DB_NAME='srpoint'

#r.db_drop(DB_NAME).run()
r.db_create(DB_NAME).run()

r.db(DB_NAME).table_create('contents').run()
r.db(DB_NAME).table_create('users').run()
r.db(DB_NAME).table_create('users_email_unique', primary_key='email').run()
r.db(DB_NAME).table_create('users_username_unique', primary_key='username').run()


r.db(DB_NAME).table('users').index_create('search', lambda row: [row['username'], row['email']], multi=True).run()

