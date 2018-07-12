CREATE TABLE `joke_more_info` (
  `title` varchar(60) DEFAULT NULL,
  `visit` int(4) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  PRIMARY KEY (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='记录没个笑话标题的游览量';
