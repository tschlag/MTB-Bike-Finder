DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  riding_type TEXT NOT NULL, 
  height TEXT NOT NULL, 
  min_budget TEXT NOT NULL, 
  max_budget TEXT NOT NULL, 
  wheel_size TEXT NOT NULL, 
  rear_sus TEXT NOT NULL, 
  country TEXT NOT NULL,
  pinkbike_url TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);