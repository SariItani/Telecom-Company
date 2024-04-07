-- Create Database
CREATE DATABASE TelecomCompany;

-- Use the database
USE TelecomCompany;

-- Create Tables with Sample Constraints (modify data types and constraints as needed)
CREATE TABLE Customers (
  CustomerID INT PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  ContactInfo VARCHAR(255) NOT NULL,
  Address VARCHAR(255)
);

CREATE TABLE Products_Services (
  ProductID INT PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  Description TEXT,
  Price DECIMAL(10,2) NOT NULL,
  Type VARCHAR(50) NOT NULL
);

CREATE TABLE Accounts (
  AccountID INT PRIMARY KEY AUTO_INCREMENT,
  CustomerID INT,
  AccountType VARCHAR(50) NOT NULL,
  AccountStatus VARCHAR(50) NOT NULL,
  BillingInfo VARCHAR(255),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Subscriptions (
  SubscriptionID INT PRIMARY KEY AUTO_INCREMENT,
  AccountID INT,
  ProductID INT,
  StartDate DATE,
  EndDate DATE,
  RenewalInfo VARCHAR(50),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID),
  FOREIGN KEY (ProductID) REFERENCES Products_Services(ProductID)
);

CREATE TABLE Orders (
  OrderID INT PRIMARY KEY AUTO_INCREMENT,
  CustomerID INT,
  OrderDate DATE,
  OrderDetails TEXT,
  OrderStatus VARCHAR(50),
  PaymentInfo VARCHAR(255),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Equipment (
  EquipmentID INT PRIMARY KEY AUTO_INCREMENT,
  ModelNumber VARCHAR(50),
  Type VARCHAR(50),
  SerialNumber VARCHAR(50),
  Status VARCHAR(50),
  AssignedTo VARCHAR(255)
);

CREATE TABLE Employees (
  EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  ContactInfo VARCHAR(255),
  Department VARCHAR(50),
  Role VARCHAR(50)
);

CREATE TABLE SupportTickets (
  TicketID INT PRIMARY KEY AUTO_INCREMENT,
  CustomerID INT,
  AccountID INT,
  DateSubmitted DATE,
  IssueDescription TEXT,
  ResolutionDetails TEXT,
  Status VARCHAR(50),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Payments (
  PaymentID INT PRIMARY KEY AUTO_INCREMENT,
  CustomerID INT,
  AccountID INT,
  PaymentDate DATE,
  Amount DECIMAL(10,2),
  PaymentMethod VARCHAR(50),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

INSERT INTO Customers (Name, ContactInfo, Address)
VALUES ('John Doe', '+1234567890', '123 Main St');

INSERT INTO Products_Services (Name, Description, Price, Type)
VALUES ('Mobile Data Plan', 'Unlimited data for smartphones', 19.99, 'Mobile');

-- Insert sample data for other tables, ensuring relationships are met
