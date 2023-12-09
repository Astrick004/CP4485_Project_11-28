DROP DATABASE IF EXISTS summarizer;
CREATE DATABASE summarizer;

USE summarizer;

CREATE TABLE user
(
	user_id			INT				PRIMARY KEY 	AUTO_INCREMENT,
    username		VARCHAR(50)		NOT NULL		UNIQUE,
    password		VARCHAR(50)		NOT NULL
) ENGINE=INNODB;

CREATE TABLE summary
(
	summary_id		INT 			PRIMARY KEY		AUTO_INCREMENT,
    created_date	Date 			NOT NULL,
    article_text	MEDIUMTEXT,
    article_url		VARCHAR(1024),
    summary_text	TEXT			NOT NULL,
    summary_length	INT,
    user_id			INT,
    CONSTRAINT summary_fk_user
		FOREIGN KEY (user_id) REFERENCES user (user_id)
) ENGINE=INNODB;
