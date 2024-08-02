/* Setup of the database */
CREATE DATABASE IF NOT EXISTS files_db_dev;
USE files_db_dev;

/* Setup of the user */
CREATE USER IF NOT EXISTS files_user_dev@localhost IDENTIFIED BY 'control_expediente';
GRANT ALL PRIVILEGES ON files_db_dev.* TO files_user_dev@localhost;
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    permission VARCHAR(20) NOT NULL,
    name VARCHAR(60) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    updated_at DATE DEFAULT (CURRENT_DATE),
    created_at DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    stage VARCHAR(50) NOT NULL,
    serial VARCHAR(50) NOT NULL,
    use_files VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    project VARCHAR(50) NOT NULL,
    num_starting VARCHAR(50) NOT NULL,
    resolution VARCHAR(50) NOT NULL,
    files VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    zone VARCHAR(255) NOT NULL,
    sector VARCHAR(50) NOT NULL,
    hood VARCHAR(50) NOT NULL,
    group_residential VARCHAR(50) NOT NULL,
    block VARCHAR(10) NOT NULL,
    lot VARCHAR(10) NOT NULL,
    last_document VARCHAR(255) NOT NULL,
    number_folio VARCHAR(10) NOT NULL,
    location_files VARCHAR(100) NOT NULL,
    observation VARCHAR(255),
    professional VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    area VARCHAR(50) NOT NULL,
    meters INT NOT NULL,       
    created_at DATE DEFAULT (CURRENT_DATE),
    updated_at DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS administered (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    type_doc VARCHAR(50) NOT NULL,
    doc_number VARCHAR(50) NOT NULL,
    phone_number VARCHAR(9),
    email VARCHAR(100),
    files_id INT NOT NULL,
    created_at DATE DEFAULT (CURRENT_DATE),
    updated_at DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (files_id) REFERENCES files(id)
);

CREATE TABLE IF NOT EXISTS professional (
    id INT AUTO_INCREMENT PRIMARY KEY,    
    name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    level VARCHAR(20),
    full_name VARCHAR(50) NOT NULL,
    created_at DATE DEFAULT (CURRENT_DATE),
    updated_at DATE DEFAULT (CURRENT_DATE)
);