CREATE TABLE tblLogs (
logID int NOT NULL auto_increment,
zone varchar(25),
logTime datetime DEFAULT NOW(),
description varchar(200) NOT null,
PRIMARY KEY (logID)
);
