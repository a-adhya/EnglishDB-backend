PRAGMA foreign_keys = ON;

CREATE TABLE Categories
(      
CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
CategoryName TEXT,
Description TEXT
);

CREATE TABLE Customers
(      
CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
CustomerName TEXT,
ContactName TEXT,
Address TEXT,
City TEXT,
PostalCode TEXT,
Country TEXT
);

CREATE TABLE Employees
(
EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
LastName TEXT,
FirstName TEXT,
BirthDate DATE,
Photo TEXT,
Notes TEXT
);

CREATE TABLE Shippers(
ShipperID INTEGER PRIMARY KEY AUTOINCREMENT,
ShipperName TEXT,
Phone TEXT
);

CREATE TABLE Suppliers(
SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
SupplierName TEXT,
ContactName TEXT,
Address TEXT,
City TEXT,
PostalCode TEXT,
Country TEXT,
Phone TEXT
);

CREATE TABLE Products(
ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
ProductName TEXT,
SupplierID INTEGER,
CategoryID INTEGER,
Unit TEXT,
Price NUMERIC DEFAULT 0,
FOREIGN KEY (CategoryID) REFERENCES Categories (CategoryID),
FOREIGN KEY (SupplierID) REFERENCES Suppliers (SupplierID)
);

CREATE TABLE Orders(
OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
CustomerID INTEGER,
EmployeeID INTEGER,
OrderDate DATETIME,
ShipperID INTEGER,
FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID),
FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID),
FOREIGN KEY (ShipperID) REFERENCES Shippers (ShipperID)
);

CREATE TABLE OrderDetails(
OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
OrderID INTEGER,
ProductID INTEGER,
Quantity INTEGER,
FOREIGN KEY (OrderID) REFERENCES Orders (OrderID),
FOREIGN KEY (ProductID) REFERENCES Products (ProductID)
);