CREATE DATABASE sina_spider;
USE sina_spider;

CREATE TABLE user_img (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uid VARCHAR(16),
    img_src VARCHAR(255)
) CHARSET=UTF8;

CREATE TABLE user_detail (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uid VARCHAR(16),
    sex VARCHAR(8),
    uname VARCHAR(255),
    fans VARCHAR(16),
    icon VARCHAR(255),
    detail text
) CHARSET=UTF8;

CREATE TABLE user_followers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    uid VARCHAR(16),
    p_uid VARCHAR(16),
    fans VARCHAR(16)
) CHARSET=UTF8;
