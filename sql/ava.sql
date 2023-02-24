CREATE TABLE avatars (
    picture bytea NOT NULL,
    user_id integer REFERENCES users(id) UNIQUE
);
