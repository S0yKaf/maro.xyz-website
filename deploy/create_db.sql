CREATE DATABASE IF NOT EXISTS `myblt` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `myblt`;

CREATE TABLE IF NOT EXISTS `uploads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hash` binary(20) NOT NULL,
  `short_url` char(7) COLLATE utf8_bin NOT NULL,
  `mime_type` varchar(255) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique` (`hash`,`short_url`),
  KEY `short_url` (`short_url`),
  KEY `hash` (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;
