CREATE DATABASE Sprinkler;

CREATE TABLE `tbllogs` (
  `logID` int(11) NOT NULL AUTO_INCREMENT,
  `relayNumber` varchar(25) DEFAULT NULL,
  `logTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(200) NOT NULL,
  PRIMARY KEY (`logID`)
);
