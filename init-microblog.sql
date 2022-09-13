CREATE SCHEMA microblog CHARACTER SET utf8 COLLATE utf8_bin;
CREATE USER 'microblog'@'%' IDENTIFIED BY 'micR0-blog-miguel';
GRANT ALL PRIVILEGES ON microblog.* TO 'microblog'@'%';
FLUSH PRIVILEGES;
