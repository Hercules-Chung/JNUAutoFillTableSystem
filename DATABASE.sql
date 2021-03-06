CREATE DATABASE JNUSTU DEFAULT SET utf8;

create table LoginData(
    user CHAR(10) NOT NULL,
    password VARCHAR(30) NOT NULL,
    Email VARCHAR(20) NOT NULL
);

CREATE TABLE UserInfo(
    user CHAR(10) NOT NULL,
    teacherName VARCHAR(20) NOT NULL,
    class VARCHAR(15) NOT NULL,
    contactName VARCHAR(20) NOT NULL,
    contactPhone VARCHAR(15) NOT NULL,
    province VARCHAR(10) NOT NULL,
    city VARCHAR(10) NOT NULL,
    area VARCHAR(10) NOT NULL,
    road VARCHAR(30) NOT NULL
);

ALTER TABLE UserInfo ADD CONSTRAINT FD_KEY FOREIGN KEY(user) REFERENCES LoginData(user) ON DELETE CASCADE;

