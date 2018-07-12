CREATE TABLE `joke_type` (
  `style` varchar(10) NOT NULL COMMENT '笑话类型',
  `number` int(4) NOT NULL COMMENT '某种类型笑话数量',
  `index_url` varchar(45) NOT NULL COMMENT '笑话类型的入口URL',
  `page` int(4) NOT NULL COMMENT '该类型笑话页数',
  PRIMARY KEY (`style`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='存储joke_types数据(类型,类型数量)';
