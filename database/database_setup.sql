CREATE DATABASE IF NOT EXISTS momoquick;

USE momoquick;

CREATE TABLE users (
    id INT PRIMARY KEY,
    full_name VARCHAR(250) NOT NULL,
    id_number INT UNIQUE
);

CREATE TABLE transaction_categories (
    id INT PRIMARY KEY,
    transaction_type VARCHAR(150) NOT NULL,
    transaction_flow ENUM('CREDIT', 'DEBIT') NOT NULL
);

CREATE TABLE transactions (
    transaction_id VARCHAR(250) PRIMARY KEY,
    user_id INT,
    category_id INT,
    message VARCHAR(250),
    amount FLOAT NOT NULL,
    transaction_date DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES transaction_categories(id)
);

CREATE TABLE system_logs (
    id INT PRIMARY KEY,
    transaction_id VARCHAR(250),
    message VARCHAR(255) NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);

INSERT INTO users (id, full_name, id_number) VALUES
(1, 'Jane Smith', '12845'),
(2, "Samuel Carter", "95464"),
(3, "Alex Doe", "43810"),
(4, "Robert Brown", "41193"),
(5, "Linda Green", "14166");

INSERT INTO transaction_categories (id, transaction_type, transaction_flow) VALUES
(1, 'Momo', 'CREDIT'),
(2, 'Momo', 'DEBIT'),
(3, 'Code', 'DEBIT'),
(4, 'Code', 'CREDIT'),
(5, 'Bank', 'DEBIT'),
(6, 'Bank', 'CREDIT');

INSERT INTO transactions (transaction_id, user_id, category_id, message, amount, transaction_date) VALUES
("0001", 1, 1, 'Payment received', 2500.00, '2024-05-21 10:00:00'),
("0002", 2, 5, 'Purchase at Store A', 75.50, '2024-07-05 14:30:00'),
("0003", 3, 4, 'Online subscription', 15.99, '2024-09-11 09:15:00'),
("0004", 4, 2, 'Refund from Store B', 40.00, '2024-10-12 16:45:00'),
("0005", 5, 3, 'Grocery shopping', 120.75, '2024-12-27 11:20:00');

INSERT INTO system_logs (id, transaction_id, message, date) VALUES
(1, "0001", 'Transaction completed successfully', '2024-05-21 10:05:00'),
(2, "0002", 'Transaction failed due to insufficient funds', '2024-07-05 14:35:00'),
(3, "0003", 'Transaction pending approval', '2024-09-11 09:20:00'),
(4, "0004", 'Transaction completed successfully', '2024-10-12 16:50:00'),
(5, "0005", 'Transaction completed successfully', '2024-12-27 11:25:00');


