<<<<<<< HEAD
CREATE DATABASE Sprinkler;

CREATE TABLE `tbllogs` (
  `logID` int(11) NOT NULL AUTO_INCREMENT,
  `relayNumber` varchar(25) DEFAULT NULL,
  `logTime` datetime DEFAULT CURRENT_TIMESTAMP,
  `description` varchar(200) NOT NULL,
  PRIMARY KEY (`logID`)
);
=======
CREATE TABLE tblLogs (
logID int NOT NULL auto_increment,
zone varchar(25),
logTime datetime DEFAULT NOW(),
description varchar(200) NOT null,
PRIMARY KEY (logID)
);
>>>>>>> a76f2598327aae3932de60dfcb3699c9c739824f
