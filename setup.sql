--
-- Example setup file for a web database project.
--

-- create database and user, grant privileges to user
create database web_database_project;
create user 'mysql_username'@'localhost' identified by 'mysql_password';
grant all on web_database_project.* to 'mysql_username'@'localhost';
flush privileges;

-- select the database and create tables
use web_database_project;
create table book(
    id int not null auto_increment primary key,
    title varchar(255) not null
);

-- insert data into database
insert into book(title) values ('How to Build a Computer');
insert into book(title) values ('How to Boot a Computer');
insert into book(title) values ('How to Reboot a Computer');
insert into book(title) values ('How to Make a Computer Do What You Want');
insert into book(title) values ('How to Turn Off a Computer');
insert into book(title) values ('How to Go Outside and Play');
