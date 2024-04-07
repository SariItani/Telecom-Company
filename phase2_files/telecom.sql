CREATE DATABASE TelecomCompany;
USE TelecomCompany;

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
  CustomerID INT NOT NULL,
  AccountType ENUM('Individual', 'Business'),
  AccountStatus ENUM('Active', 'Inactive'),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Subscriptions (
  SubscriptionID INT PRIMARY KEY AUTO_INCREMENT,
  AccountID INT NOT NULL,
  ProductID INT NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE,
  RenewalInformation ENUM('Automatic', 'Manual'),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID),
  FOREIGN KEY (ProductID) REFERENCES Products_Services(ProductID)
);

CREATE TABLE Orders (
  OrderID INT PRIMARY KEY AUTO_INCREMENT,
  AccountID INT NOT NULL,
  Date DATE NOT NULL,
  OrderDetails TEXT,
  OrderStatus ENUM('Pending', 'Processing', 'Completed', 'Cancelled'),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

-- Payments Table
CREATE TABLE Payments (
  PaymentID INT PRIMARY KEY AUTO_INCREMENT,
  AccountID INT,
  Date DATE NOT NULL,
  Amount DECIMAL(10,2) NOT NULL,
  PaymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'Other'),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Equipment (
  EquipmentID INT PRIMARY KEY AUTO_INCREMENT,
  ModelNumber VARCHAR(50) NOT NULL,
  Type VARCHAR(50) NOT NULL,
  SerialNumber VARCHAR(50) NOT NULL,
  Status ENUM('Active', 'Inactive', 'Loaned'),
  AssignedAccountID INT,
  FOREIGN KEY (AssignedAccountID) REFERENCES Accounts(AccountID)
);

CREATE TABLE Employees (
  EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
  Name VARCHAR(255) NOT NULL,
  ContactInfo VARCHAR(255) NOT NULL,
  Department VARCHAR(50) NOT NULL,
  Role VARCHAR(50) NOT NULL
);

CREATE TABLE SupportTickets (
  TicketID INT PRIMARY KEY AUTO_INCREMENT,
  AccountID INT,
  DateSubmitted DATE NOT NULL,
  IssueDescription TEXT NOT NULL,
  ResolutionDetails TEXT,
  Status ENUM('Open', 'Closed'),
  FOREIGN KEY (AccountID) REFERENCES Accounts(AccountID)
);


INSERT INTO Customers (Name, ContactInfo, Address)
VALUES ('John Doe', '+1234567890', '123 Main St');

INSERT INTO Products_Services (Name, Description, Price, Type)
VALUES ('Mobile Data Plan', 'Unlimited data for smartphones', 19.99, 'Mobile');

-- ... Insert sample data for
