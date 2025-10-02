# 📘 MomoTransaction REST API Documentation


This API allows clients to manage **MoMo Quick transactions** across multiple tables (`Momo_credit`, `Momo_debit`, `Agent`, `Bank_Deposit`, `MTN_Bundle`,`Utilities`).  
Authentication is required for all endpoints.


---


## 🔐 Authentication
- **Scheme:** HTTP Basic Authentication  
- **Header format:**  
```


Authorization: Basic <base64(username:password)>


````
- Example:
```sh
curl -u admin:secret http://localhost:8000/transactions
````


---


## 📍 Endpoints


### 1. Get All Transactions


**Endpoint:**


```
GET /transactions
```


**Request Example:**


```sh
curl -u admin:secret http://localhost:8000/transactions
```


**Response Example:**


```json
{
  "momoquick": [
    {
      "Momo_credit": [
        {
            "Transaction_ID": "MC-001",
            "Name": "Jane Smith",
            "Amount": 2000,
            "Date": "2024-05-10 16:30:51"
        }
      ]
    },
    {
      "Momo_debit": []
    }
  ]
}
```


**Error Codes:**


* `401 Unauthorized` – Missing or invalid authentication


---


### 2. Get Single Transaction


**Endpoint:**


```
GET /transactions/{table}/{transaction_id}
```


**Request Example:**


```sh
curl -u admin:secret http://localhost:8000/transactions/Momo_credit/MC-001
```


**Response Example:**


```json
{
  "Transaction_ID": "MC-001",
  "Name": "Jane Smith",
  "amount": 2000,
  "date": "2024-05-10 16:30:51"
}
```


**Error Codes:**


* `401 Unauthorized` – Invalid credentials
* `404 Not Found` – Table or transaction not found


---


### 3. Add a New Transaction


**Endpoint:**


```
POST /transactions
```


**Request Body:**


```json
{
  "table": "Momo_credit",
  "record": {
    "Name":"Jonny Bravo",
    "amount": 5000,
    "date": "2025-10-02 16:30:51"
  }
}
```


**Request Example:**


```sh
curl -u admin:secret -X POST http://localhost:8000/transactions \
-H "Content-Type: application/json" \
-d '{
  "table": "Momo_credit",
  "record": {
    "Name": "Jonny Bravo"
    "amount": 5000,
    "date": "2025-10-02 16:30:51"
  }
}'
```


**Response Example:**


```json
{
  "message": "Transaction added",
  "Transaction_ID": "MC-002"
}
```


**Error Codes:**


* `400 Bad Request` – Missing `table` or `record`
* `404 Not Found` – Table not found


---


### 4. Update a Transaction


**Endpoint:**


```
PUT /transactions
```


**Request Body:**


```json
{
  "table": "Momo_credit",
  "Transaction_ID": "MC-002",
  "updates": {
    "amount": 6000
  }
}
```


**Request Example:**


```sh
curl -u admin:secret -X PUT http://localhost:8000/transactions \
-H "Content-Type: application/json" \
-d '{
  "table": "Momo_credit",
  "Transaction_ID": "MC-002",
  "updates": { "amount": 6000 }
}'
```


**Response Example:**


```json
{
  "message": "Transaction MC-002 updated"
}
```


**Error Codes:**


* `400 Bad Request` – Missing required fields
* `404 Not Found` – Transaction or table not found


---


### 5. Delete a Transaction


**Endpoint:**


```
DELETE /transactions/{table}/{transaction_id}
```


**Request Example:**


```sh
curl -u admin:secret -X DELETE http://localhost:8000/transactions/Momo_credit/MC-002
```


**Response Example:**


```json
{
  "message": "Transaction MC-002 deleted"
}
```


**Error Codes:**


* `400 Bad Request` – Wrong path format
* `404 Not Found` – Transaction or table not found


---


## ⚠️ Error Response Format


All errors return JSON in this format:


```json
{
  "error": "Message describing the issue"
}
```


---

