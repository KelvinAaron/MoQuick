CREATE DATABASE IF NOT EXISTS momoquick;

USE momoquick;
-- USERS TABLE
CREATE TABLE Users (
    User_Id VARCHAR(250) PRIMARY KEY,
    Name VARCHAR(250) NOT NULL,
    Type ENUM('code', 'phone_number') NOT NULL,
    Number INT NOT NULL
);

-- MOMO DEBIT
CREATE TABLE Momo_Debit (
    Transaction_Id VARCHAR(250) PRIMARY KEY,
    UserId VARCHAR(250) NOT NULL,
    Amount INT NOT NULL,
    Date DATETIME NOT NULL,
    Fee INT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Users (User_Id)
);

-- AGENT
CREATE TABLE Agent (
    Transaction_Id INT PRIMARY KEY,
    Agent_Id INT NOT NULL,
    Amount INT NOT NULL,
    Date DATETIME NOT NULL,
    Fee INT NOT NULL
    FOREIGN KEY (Agent_Id) REFERENCES Users (User_Id)
);

-- MOMO CREDIT
CREATE TABLE Momo_Credit (
    Transaction_Id VARCHAR(250) PRIMARY KEY,
    Name VARCHAR(250) NOT NULL,
    Amount INT NOT NULL,
    Date DATETIME NOT NULL
);

-- BANK DEPOSIT
CREATE TABLE Bank_Deposit (
    Transaction_Id VARCHAR(250) PRIMARY KEY,
    Amount INT NOT NULL,
    Date DATETIME NOT NULL
);

-- UTILITIES
CREATE TABLE Utilities (
    Transaction_Id VARCHAR(250) PRIMARY KEY,
    Name VARCHAR(250) NOT NULL,
    Amount INT NOT NULL,
    Fee INT NOT NULL,
    Date DATETIME NOT NULL
);

-- MTN BUNDLE
CREATE TABLE MTN_Bundle (
    Transaction_Id VARCHAR(250) PRIMARY KEY,
    Type ENUM('AIRTIME', 'DATA') NOT NULL,
    Bundle_Amount VARCHAR(250),
    Amount INT NOT NULL,
    Fee INT NOT NULL,
    Date DATETIME NOT NULL
);


