CREATE SCHEMA `shuttleapp`;
CREATE SCHEMA `test_shuttleapp`;
CREATE USER 'backoffice_user'@'%' WITH PASSWORD 'qwerty';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA shuttleapp.* TO 'backoffice_user'@'%';
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA test_shuttleapp.* TO 'backoffice_user'@'%';
