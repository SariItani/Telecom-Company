-- database creation

CREATE DATABASE IF NOT EXISTS TELECOM;

USE TELECOM;

CREATE TABLE IF NOT EXISTS Customers (
  cid INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(50) NOT NULL,
  contact_info VARCHAR(50) NOT NULL,
  customer_address VARCHAR(50) NOT NULL,
  PRIMARY KEY (cid)
);

CREATE TABLE IF NOT EXISTS Accounts (
  aid INT NOT NULL AUTO_INCREMENT,
  cid INT NOT NULL,
  account_type ENUM('Individual','Business'),
  account_status ENUM('Active','Inactive'),
  PRIMARY KEY (aid),
  FOREIGN KEY (cid) REFERENCES Customers(cid)
);

CREATE TABLE IF NOT EXISTS Services (
  pid INT NOT NULL AUTO_INCREMENT,
  service_name VARCHAR(50) NOT NULL,
  description VARCHAR(50) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (pid)
);

CREATE TABLE IF NOT EXISTS SIM_Cards (
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

CREATE TABLE IF NOT EXISTS Subscriptions (
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

CREATE TABLE IF NOT EXISTS Support_Tickets (
  tid INT NOT NULL AUTO_INCREMENT,
  aid INT NOT NULL,
  issue_description VARCHAR(50) NOT NULL,
  ticket_status ENUM('Active', 'Inactive'),
  resolution_details VARCHAR(50),
  PRIMARY KEY (tid),
  FOREIGN KEY (aid) REFERENCES Accounts(aid)
);

CREATE TABLE IF NOT EXISTS Employees (
  eid INT NOT NULL AUTO_INCREMENT,
  employee_name VARCHAR(50) NOT NULL,
  contact_info VARCHAR(50) NOT NULL,
  employee_address VARCHAR(50) NOT NULL,
  department ENUM('POS', 'Site', 'Warehouse'),
  job_title VARCHAR(50) NOT NULL,
  PRIMARY KEY (eid)
);

CREATE TABLE IF NOT EXISTS Payments (
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

CREATE TABLE IF NOT EXISTS Departments (
  did INT NOT NULL AUTO_INCREMENT,
  eid INT NOT NULL,
  department_description VARCHAR(50),
  capacity INT,
  department_address VARCHAR(50) NOT NULL,
  department_name ENUM('POS', 'Site', 'Warehouse'),
  PRIMARY KEY (did),
  FOREIGN KEY (eid) REFERENCES Employees(eid)
);

CREATE TABLE IF NOT EXISTS Equipment (
  eqid INT NOT NULL AUTO_INCREMENT,
  equipment_name VARCHAR(50) NOT NULL,
  model VARCHAR(50) NOT NULL,
  department ENUM('POS', 'Site', 'Warehouse'),
  equipment_status ENUM('Active', 'Inactive'),
  PRIMARY KEY (eqid)
);

ALTER TABLE Customers
ADD COLUMN password_hash VARCHAR(255) NOT NULL;

ALTER TABLE Employees
ADD COLUMN password_hash VARCHAR(255) NOT NULL;


-- -- sample testing data

-- INSERT INTO Customers (customer_name, contact_info, customer_address) VALUES
-- ('John Doe', '+1234567890', '123 Main St'),
-- ('Jane Smith', '+9876543210', '456 Elm St');

-- INSERT INTO Accounts (cid, account_type, account_status) VALUES
-- (1, 'Individual', 'Active'),
-- (2, 'Business', 'Inactive');

-- INSERT INTO Services (service_name, description, price) VALUES
-- ('Mobile Data Plan', 'Unlimited data for smartphones', 19.99),
-- ('Internet Plan', 'High-speed internet access', 29.99),
-- ('TV Package', 'Streaming TV channels', 39.99);

-- INSERT INTO SIM_Cards (IMSI, aid, phone_number, sim_status, ICCID, PUK, PIN) VALUES
-- (123456789, 1, '+1234567890', 'Active', '1234567890123456', '123456', '789012'),
-- (987654321, 2, '+9876543210', 'Inactive', '9876543210987654', '654321', '098765');

-- INSERT INTO Subscriptions (pid, IMSI, starting_date, ending_date, renewal) VALUES
-- (1, 123456789, '2024-01-01', '2024-12-31', 'Auto'),
-- (2, 987654321, '2024-02-01', '2024-11-30', 'Manual');

-- INSERT INTO Support_Tickets (aid, issue_description, ticket_status, resolution_details) VALUES
-- (1, 'Slow internet connection', 'Active', 'Technician dispatched'),
-- (2, 'No network coverage', 'Inactive', 'N/A');

INSERT INTO Employees (employee_name, contact_info, employee_address, department, job_title) VALUES
('root', '+96181192894', 'Aramoun, Mount Lebanon, Lebanon', 'Site', 'Manager'),
-- ('Bob Smith', '+9988776655', '456 Pine St', 'Site', 'Technician'),
-- ('Charlie Brown', '+5544332211', '123 Maple St', 'Warehouse', 'Manager'),
-- ('David Mason', 'mason@gmail.com', '564 Mason St', 'POS', 'Manager'),
-- ('Satan', 'the devil', '666 Devil St', 'Site', 'Manager');

-- INSERT INTO Payments (aid, eid, sub_id, due_date, amount, payment_method, payment_date) VALUES
-- (1, 1, 1, '2024-03-15', 19.99, 'Credit Card', '2024-03-15'),
-- (2, 2, 2, '2024-03-20', 29.99, 'Cash', '2024-03-20');

-- INSERT INTO Departments (eid, department_description, capacity, department_address, department_name) VALUES
-- (3, 'Point of Sales', NULL, '789 Oak St', 'POS'),
-- (4, 'Network Site', 50, '456 Pine St', 'Site'),
-- (5, 'Equipment Warehouse', 200, '123 Maple St', 'Warehouse');

-- INSERT INTO Equipment (equipment_name, model, department, equipment_status) VALUES
-- ('Modem', 'ABC123', 'POS', 'Active'),
-- ('Router', 'XYZ456', 'Site', 'Inactive'),
-- ('Antenna', '123ABC', 'Warehouse', 'Active');


-- -- Sample Queries to Test the Telecom Database

-- SELECT * FROM Customers;

-- SELECT * FROM Accounts WHERE account_status = 'Active';

-- SELECT * FROM Services WHERE price < 30;

-- SELECT * FROM SIM_Cards WHERE sim_status = 'Active';

-- SELECT * FROM Subscriptions WHERE renewal = 'Auto';

-- SELECT * FROM Support_Tickets WHERE ticket_status = 'Active';

-- SELECT * FROM Departments WHERE capacity > 100;

-- SELECT service_name, price FROM Services;

-- SELECT * FROM SIM_Cards;

-- SELECT * FROM Subscriptions;

-- SELECT * FROM Support_Tickets;

-- SELECT * FROM Employees WHERE department = 'POS';

-- SELECT * FROM Payments WHERE payment_method = 'Credit Card';

-- SELECT department_name, capacity FROM Departments;

-- SELECT * FROM Equipment WHERE equipment_status = 'Active';

-- SELECT customer_name, contact_info
-- FROM Customers
-- WHERE cid IN (
--   SELECT cid
--   FROM Accounts
--   WHERE account_status = 'Active'
-- );

-- SELECT IMSI, ICCID
-- FROM SIM_Cards
-- WHERE sim_status = 'Inactive';

-- SELECT Subscriptions.pid, Services.service_name, Subscriptions.starting_date, Subscriptions.ending_date, Subscriptions.renewal
-- FROM Subscriptions
-- INNER JOIN Services ON Subscriptions.pid = Services.pid
-- WHERE Subscriptions.renewal = 'Auto';

-- SELECT st.tid, st.issue_description, c.customer_name
-- FROM Support_Tickets st
-- INNER JOIN Accounts a ON st.aid = a.aid
-- INNER JOIN Customers c ON a.cid = c.cid
-- WHERE st.ticket_status = 'Active';

-- SELECT employee_name, job_title
-- FROM Employees
-- WHERE department = 'Site';

-- SELECT SUM(amount) AS total_collected
-- FROM Payments
-- WHERE payment_method = 'Credit Card';

-- SELECT service_name, description
-- FROM Services;

-- SELECT Accounts.account_type, SUM(Payments.amount) AS total_paid
-- FROM Accounts
-- INNER JOIN Payments ON Accounts.aid = Payments.aid
-- WHERE Accounts.account_status = 'Active'
-- GROUP BY Accounts.account_type;
