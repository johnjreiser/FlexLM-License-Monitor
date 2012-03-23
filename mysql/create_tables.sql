delimiter $$

CREATE TABLE `license_monitor` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(20) DEFAULT NULL,
  `computer` varchar(20) DEFAULT NULL,
  `license` varchar(20) DEFAULT NULL,
  `time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `action` tinyint(4) DEFAULT NULL,
  `uid` varchar(62) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `UID` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=14458 DEFAULT CHARSET=utf8$$

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `UsersOnline` AS select `license_monitor`.`user` AS `user`,`license_monitor`.`computer` AS `computer`,`license_monitor`.`license` AS `license`,`license_monitor`.`uid` AS `uid`,sum(`license_monitor`.`action`) AS `STATUS`,max(`license_monitor`.`time`) AS `TIME` from `license_monitor` group by `license_monitor`.`uid`$$

CREATE TABLE `raw_users` (
  `timeid` int(11) NOT NULL AUTO_INCREMENT,
  `YEAR` int(11) DEFAULT NULL,
  `MONTH` int(11) DEFAULT NULL,
  `DAY` int(11) DEFAULT NULL,
  `DOW` varchar(10) DEFAULT NULL,
  `HOUR` int(11) DEFAULT NULL,
  `MINUTE` int(11) DEFAULT NULL,
  `TOTALROBIN` int(11) DEFAULT NULL,
  `TOTALCLOUD` int(11) DEFAULT NULL,
  PRIMARY KEY (`timeid`),
  UNIQUE KEY `timeid_UNIQUE` (`timeid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8$$


