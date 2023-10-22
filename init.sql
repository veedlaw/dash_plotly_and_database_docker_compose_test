USE mydb;
CREATE TABLE IF NOT EXISTS options (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255));
INSERT INTO options (name) VALUES ('Option 1'), ('Option 2'), ('Option 3');

