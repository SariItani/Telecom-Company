CREATE DATABASE TELECOM;

USE TELECOM

CREATE TABLE Customers (
  cid INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NOT NULL,
  ContactInfo VARCHAR(50) NOT NULL,
  Address VARCHAR(50) NOT NULL,
  PRIMARY KEY (cid)
);

CREATE TABLE Accounts (
  aid INT NOT NULL AUTO_INCREMENT,
  cid INT NOT NULL,
  AccountType ENUM('Individual','Business'),
  Status ENUM('Active','Inactive'),
  PRIMARY KEY (aid),
  FOREIGN KEY (cid) REFERENCES Customers(cid)
);

CREATE TABLE Services (
  pid INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NOT NULL,
  Description VARCHAR(150) NOT NULL,
  Price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (pid)
);

CREATE TABLE SIM_Cards (
  IMSI VARCHAR(50) NOT NULL,
  aid INT NOT NULL,
  Phone_Number VARCHAR(50) NOT NULL,
  Status ENUM('Active', 'Inactive'),
  ICCID VARCHAR(50) NOT NULL,
  PUK VARCHAR(50) NOT NULL,
  PIN VARCHAR(50) NOT NULL,
  PRIMARY KEY (IMSI),
  UNIQUE (ICCID),
  UNIQUE (PUK),
  UNIQUE (PIN),
  FOREIGN KEY (aid) REFERENCES Accounts(aid)
);

CREATE TABLE Subscriptions (
  sub_id INT NOT NULL AUTO_INCREMENT,
  pid INT NOT NULL,
  IMSI VARCHAR(50) NOT NULL,
  Start_Date DATE NOT NULL,
  End_Date DATE NOT NULL,
  Renewal ENUM('Auto', 'Manual'),
  PRIMARY KEY (sub_id),
  FOREIGN KEY (pid) REFERENCES Services(pid),
  FOREIGN KEY (IMSI) REFERENCES SIM_Cards(IMSI)
);

CREATE TABLE Support_Tickets (
  tid INT NOT NULL AUTO_INCREMENT,
  aid INT NOT NULL,
  IssueDescription VARCHAR(150) NOT NULL,
  Status ENUM('Active', 'Inactive'),
  ResolutionDetails VARCHAR(150),
  PRIMARY KEY (tid),
  FOREIGN KEY (aid) REFERENCES Accounts(aid)
);

CREATE TABLE Employees (
  eid INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NOT NULL,
  ContactInfo VARCHAR(50) NOT NULL,
  Address VARCHAR(50) NOT NULL,
  Department ENUM('POS', 'Site', 'Warehouse'),
  Job_Title VARCHAR(50) NOT NULL,
  PRIMARY KEY (eid)
);

CREATE TABLE Payments (
  pay_id INT NOT NULL AUTO_INCREMENT,
  aid INT NOT NULL,
  eid INT,
  sub_id INT,
  Due_Date DATE NOT NULL,
  Amount DECIMAL(10,2) NOT NULL,
  Method ENUM('Credit Card', 'Cash'),
  Date DATE,
  PRIMARY KEY (pay_id),
  FOREIGN KEY (aid) REFERENCES Accounts(aid),
  FOREIGN KEY (eid) REFERENCES Employees(eid),
  FOREIGN KEY (sub_id) REFERENCES Subscriptions(sub_id)
);

CREATE TABLE Departments (
  did INT NOT NULL AUTO_INCREMENT,
  eid INT NOT NULL,
  Description VARCHAR(150),
  Capacity INT,
  Address VARCHAR(50) NOT NULL,
  Name ENUM('POS', 'Site', 'Warehouse'),
  PRIMARY KEY (did),
  FOREIGN KEY (eid) REFERENCES Employees(eid)
);

CREATE TABLE Equipment (
  eqid INT NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NOT NULL,
  Model VARCHAR(50) NOT NULL,
  Department ENUM('POS', 'Site', 'Warehouse'),
  Status ENUM('Active', 'Inactive'),
  PRIMARY KEY (eqid)
);
