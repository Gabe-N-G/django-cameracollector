CREATE DATABASE cameracollector;

CREATE USER camera_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE cameracollector TO camera_admin;