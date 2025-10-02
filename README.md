## Senior Devs
### Members:
1.    Aaron-Onuigbo Kelvin
2.    Isimbi Nelly Assoumpta
3.    Jonathan Mugisha
4.    Junior Nkuba Igiraneza

We are a team of software engineers working together to create a simple budget planning app synced with the users momo.

MoQuick is an application that sorts financial data from and XML data source and displays such data in an ordered format on the web. It can be used to help users organise their spendings done through momo for easy financial planning.

### Documentation:
The Database has 7 tables (Users, Momo_Debit, Agent, Momo_Credit, Bank_Deposit, Utilities and MTN_Bundle).

The **Momo_Debit and Agent tables** will use users from the Users table to store data for a particular transaction from the xml data and will be provided an id upon creation to serve as the primary key.

The **Momo_Credit** will store the variuos kinds of transactions where money was credited into the momo account from individuals.

The **Bank_Deposit** will store data related to deposited money from banks into the momo account.

The **MTN_Bundle** will store data on transactions where the user bought mtn airtime or data bundles.

The **Utilities** will store all other data the user paid to for various utilities from electricity to water and various fee with the fee noted in the table under the name column.

Here is a simple test of CRUD operations returned after running the database_setup.sql script

![alt text](https://github.com/KelvinAaron/MoQuick/blob/main/screenshots/demo.png) 

#### JSON Representation:
From the JSON example in /examples in the first momoquick object we see how each tables columns and attribute is represented as keys and value in the JSON. The user table show the columns (id, full_name, id_number) and their values for one record in the table (1, Jane Smith, 12845).

The second object demonstrates a complex object of the **transactions table** showing how the foerign key points to the specific record from both the **users** and **transaction categories** table.

#### SMS Records in JSON:
To parse the xml modified_sms_v2.xml data into json you need to first create a .env file and setup "USER_NAME" and "PASSWORD" variables then run the api.py file in /api. You can then access the server running on port 8000 by visiting the endpoints documented in /docs/api_docs.md.

### Architectural Design:

![alt text](https://github.com/KelvinAaron/MoQuick/blob/main/screenshots/Architectural.png) 

[Scrum Board](https://github.com/users/KelvinAaron/projects/1/views/1)
