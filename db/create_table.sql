CREATE TABLE IF NOT EXISTS weather (
  id serial PRIMARY KEY,
  t_bme680 NUMERIC (7,4) NOT NULL,
  t_sht31d NUMERIC (7,4) NOT NULL,
  h_bme680 NUMERIC (7,4) NOT NULL,
  h_sht31d NUMERIC (7,4) NOT NULL,
  pressure NUMERIC (6,2) NOT NULL,
  created_at timestamptz DEFAULT CURRENT_TIMESTAMP
);

