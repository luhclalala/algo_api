CREATE DATABASE IF NOT EXISTS 202_schema;
USE 202_schema;

CREATE TABLE IF NOT EXISTS qa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_id VARCHAR(255) UNIQUE,
    query TEXT,
    result TEXT
); 