CREATE TABLE IF NOT EXISTS weather (
  id INTEGER PRIMARY KEY,
  temperature REAL NOT NULL,
  humidity REAL NOT NULL,
  pressure REAL NOT NULL,
  delta REAL NOT NULL,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP
);
