CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  email TEXT,
  password TEXT,
  role TEXT
);

CREATE TABLE predictions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  risk REAL,
  tier TEXT,
  no_antibiotic REAL,
  with_antibiotic REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
