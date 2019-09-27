--DROP TABLE IF EXISTS "user" cascade ;
--DROP TABLE IF EXISTS "post" cascade ;

 CREATE TABLE IF NOT EXISTS "user" (
  id serial PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "post" (
  id serial PRIMARY KEY ,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES "user" (id)
);