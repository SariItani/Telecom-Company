CREATE DATABASE IF NOT EXISTS TELECOM;

USE TELECOM;

CREATE TABLE Customers (
  cid INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(50) NOT NULL,
  contact_info VARCHAR(50) NOT NULL,
  customer_address VARCHAR(50) NOT NULL,
  PRIMARY KEY (cid)
);

CREATE TABLE Accounts (
  aid INT NOT NULL AUTO_INCREMENT,
  cid INT NOT NULL,
  account_type ENUM('Individual','Business'),
  account_status ENUM('Active','Inactive'),
  PRIMARY KEY (aid),
  FOREIGN KEY (cid) REFERENCES Customers(cid)
);

CREATE TABLE Services (
  pid INT NOT NULL AUTO_INCREMENT,
  service_name VARCHAR(50) NOT NULL,
  description VARCHAR(50) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (pid)
);

CREATE TABLE SIM_Cards (
  IMSI VARCHAR(50) NOT NULL,
  aid INT, -- Could be NULL if the SIM Card exists but is not linked to any account yet.
  phone_number VARCHAR(50) NOT NULL,
  sim_status ENUM('Active', 'Inactive'),
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
  starting_date DATE NOT NULL,
  ending_date DATE NOT NULL,
  renewal ENUM('Auto', 'Manual'),
  PRIMARY KEY (sub_id),
  FOREIGN KEY (pid) REFERENCES Services(pid),
  FOREIGN KEY (IMSI) REFERENCES SIM_Cards(IMSI)
);

CREATE TABLE Support_Tickets (
  tid INT NOT NULL AUTO_INCREMENT,
  aid INT NOT NULL,
  issue_description VARCHAR(50) NOT NULL,
  ticket_status ENUM('Active', 'Inactive'),
  resolution_details VARCHAR(50),
  PRIMARY KEY (tid),
  FOREIGN KEY (aid) REFERENCES Accounts(aid)
);

CREATE TABLE Employees (
  eid INT NOT NULL AUTO_INCREMENT,
  employee_name VARCHAR(50) NOT NULL,
  contact_info VARCHAR(50) NOT NULL,
  employee_address VARCHAR(50) NOT NULL,
  department ENUM('POS', 'Site', 'Warehouse'),
  job_title VARCHAR(50) NOT NULL,
  PRIMARY KEY (eid)
);

CREATE TABLE Payments (
  payment_id INT NOT NULL AUTO_INCREMENT,
  aid INT NOT NULL,
  eid INT,
  sub_id INT,
  due_date DATE NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  payment_method ENUM('Credit Card', 'Cash'),
  payment_date DATE,
  PRIMARY KEY (payment_id),
  FOREIGN KEY (aid) REFERENCES Accounts(aid),
  FOREIGN KEY (eid) REFERENCES Employees(eid),
  FOREIGN KEY (sub_id) REFERENCES Subscriptions(sub_id)
);

CREATE TABLE Departments (
  did INT NOT NULL AUTO_INCREMENT,
  eid INT NOT NULL,
  department_description VARCHAR(50),
  capacity INT,
  department_address VARCHAR(50) NOT NULL,
  department_name ENUM('POS', 'Site', 'Warehouse'),
  PRIMARY KEY (did),
  FOREIGN KEY (eid) REFERENCES Employees(eid)
);

CREATE TABLE Equipment (
  eqid INT NOT NULL AUTO_INCREMENT,
  equipment_name VARCHAR(50) NOT NULL,
  model VARCHAR(50) NOT NULL,
  department ENUM('POS', 'Site', 'Warehouse'),
  equipment_status ENUM('Active', 'Inactive'),
  PRIMARY KEY (eqid)
);
