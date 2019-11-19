CREATE TABLE IF NOT EXISTS "user" (
    id serial PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN
);

CREATE TABLE IF NOT EXISTS "post" (
    id serial PRIMARY KEY,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES "user" (id)
);

CREATE TABLE IF NOT EXISTS "follower" (
    follower_id INT,
    followed_id INT NOT NULL,
    PRIMARY KEY (follower_id, followed_id),
    FOREIGN KEY (follower_id) REFERENCES "user" (id)
);

CREATE TABLE IF NOT EXISTS "movie" (
    movie_id INT NOT NULL PRIMARY KEY,
    vote_count BIGINT NOT NULL,
    vote_average BIGINT not null,
    fav_count BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS "watched_movies" (
    user_id INT NOT NULL,
    movie_id INT NOT NULL,
    favorite BOOLEAN,
    rate FLOAT,
    PRIMARY KEY (user_id, movie_id),
    FOREIGN KEY (user_id) REFERENCES "user" (id),
    FOREIGN KEY (movie_id) REFERENCES "movie" (movie_id)
);