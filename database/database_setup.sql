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
    Transaction_Id VARCHAR(250) PRIMARY KEY,
    Agent_Id VARCHAR(250) NOT NULL,
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

INSERT INTO Users (User_Id, Name, Type, Number) VALUES
('U-001', 'Jane Smith', 'code', 12845),
('U-002', 'Samuel Carter', 'phone_number', 250791666666),
('U-003', 'Sophia', 'phone_number', 250790777777),
('U-004', 'John', 'phone_number', 250788999999),
('U-005', 'Linda Green', 'code', 75028);

INSERT INTO Momo_Debit (Transaction_Id, UserId, Amount, Date, Fee) VALUES
('MB-001', 'U-001', 1000, '2024-05-10 16:31:39', 0),
('MB-002', 'U-002', 10000, '2024-05-11 20:34:47', 100),
('MB-003', 'U-003', 5000, '2024-05-12 18:08:58', 0);

INSERT INTO Agent (Transaction_Id, Agent_Id, Amount, Date, Fee) VALUES
('AG-001', 'U-004', 20000, '2024-05-26 02:10:27', 350),
('AG-002', 'U-005', 24000, '2024-11-23 14:09:27', 600);

INSERT INTO Momo_Credit (Transaction_Id, Name, Amount, Date) VALUES
('MC-001', 'Jane Smith', 2000, '2024-05-10 16:30:51'),
('MC-002', 'Samuel Carter', 25000, '2024-05-14 20:57:36');




