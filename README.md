## Senior Devs
### Members:
1.    Aaron-Onuigbo Kelvin
2.    Isimbi Nelly Assoumpta
3.    Jonathan Mugisha
4.    Junior Nkuba Igiraneza

We are a team of software engineers working together to create a simple budget planning app synced with the users momo.

MoQuick is an application that sorts financial data from and XML data source and displays such data in an ordered format on the web. It can be used to help users organise their spendings done through momo for easy financial planning.

### Documentation:
The Database has 4 tables (users, transaction categories, transactions and system logs).

The **users table** will store data about the various the owner has interated in the various transactions from the xml data and will be provided an id upon creation to serve as the primary key.

The **transaction categories table** will store the variuos kinds of transaction that can take place i.e momo to momo, momo to bank, momo to code both ways for each. So it will have a total of exaclty 6 records as a momo to momo transaction can either be the owner recieving money(credit) or sending out money(debit).

The **transactions table** will then bring together data from the user and the transactions with foreign keys to store data about a transaction including the amount transacted, message and the date.

The status of the transaction is then logged in the **system logs table** it tracks if a transaction was successful, pending or failed with the response saved.

Here is a simple test of CRUD operations returned after running the database_setup.sql script

![alt text](https://github.com/KelvinAaron/MoQuick/blob/main/docs/demo.png) 

#### JSON Representation:
From the JSON example in /examples in the first momoquick object we see how each tables columns and attribute is represented as keys and value in the JSON. The user table show the columns (id, full_name, id_number) and their values for one record in the table (1, Jane Smith, 12845).

The second object demonstrates a complex object of the **transactions table** showing how the foerign key points to the specific record from both the **users** and **transaction categories** table.

### Architectural Design:

![alt text](https://github.com/KelvinAaron/MoQuick/blob/main/docs/Architectural.png) 

[Scrum Board](https://github.com/users/KelvinAaron/projects/1/views/1)
