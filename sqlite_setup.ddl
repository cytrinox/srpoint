CREATE TABLE resouces
(
	id				TEXT PRIMARY KEY NOT NULL,
	content			CLOB,
	CONSTRAINT		content_valid CHECK(json_valid(content)),
	CONSTRAINT		content_match_id CHECK(json_extract(content, '$.id') = id)
);

CREATE TABLE users
(
	id				TEXT PRIMARY KEY NOT NULL,
	content 		CLOB,
	CONSTRAINT		content_valid CHECK(json_valid(content)),
	CONSTRAINT		content_match_id CHECK(json_extract(content, '$.id') = id),
	CONSTRAINT		content_email_null CHECK(json_extract(content, '$.email') NOT NULL),
	CONSTRAINT		content_username_null CHECK(json_extract(content, '$.username') NOT NULL)
);

CREATE INDEX idx_users_unique_email ON users(json_extract(content, '$.email'));
CREATE INDEX idx_users_unique_username ON users(json_extract(content, '$.username'));



PRAGMA user_version = 1;

