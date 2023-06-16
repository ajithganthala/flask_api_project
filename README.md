# python_flask_sql_toystore_api_project

**Description:**

A Soft Toy Online store, which contains the details of the toys like ID, Name, Description, Price and Quantity, all the details of the toy is stored in MySQL Database and is managed by Python through Flask API where we can Insert a Toy(Post Method), Update Toy(PUT Method), Display Toy Catalog(Get Method), Delete a Specific Toy with ID(Delete Method), Search Toy with Name(Get Method), Get Details of the Toy with ID(Get Method),

**Dependencies to Run the Project:**

1. Install MySQL on the System and run the below query in SQL,
   
   CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
   
   GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost' WITH GRANT OPTION;
   
   FLUSH PRIVILEGES;

   The above query will create a user with Password and will grant all access to the created user
   
3. From the repo download and run the **pckg_installer.py** file, to run the file, please go to cmd prompt and use the command - **python pckg_installer.py**, this will install all the necessary libraries required to run the source code.
   
4. Now, download the source code - **toys_script.py**, run the source code by using command - **python toys_script.py** in the cmd promt, if code runs successfully the line - **Running on http://127.0.0.1:5000** will be displayed, then follow below api methods to use the project

5. To use api calls, I used Postman (can be downloaded from here - https://www.postman.com/downloads/

Flask Api End Points in this Project:

1. Method - POST:
   
   Source Code Function - create_toy()

   Scenario 1:
   The above method and fucntion will create a toy(Unique ID with every entry, generated automatically) in the sql database and returns the below image output and status code - 201
   
   The API Url,Input and Ouptut can be seen in the image
   ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/ee645cac-d72f-4b85-ab3e-f9fa304c94e6)

   Scenario 2:
   If the toy already exists, will check this condtion with Name, Description and Price of the toy, if exists the output from API will be shown in the below image and status code - 409
   
   The API Url,Input and Ouptut can be seen in the image
   ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/2c7b0c92-0805-4efb-9dc4-4e37e85329a4)

   Scenario 3:
   The api will return status code - 400 if data is not provided correctly and 500 if database error

2. Method - PUT:

   Source Code Function - update_toy(toy_id)

   Scenario 1:
   The above method and fucntion will update the toy with the Toy ID, will retunr the output and status code - 200
   
   The API Url,Input and Ouptut can be seen in the image
   ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/84d27281-caaa-4344-800f-c2c4be69f4fb)

   Scenario 2:
   If the toy doesn't exists with ID while updation, it will return the below output and status code - 404
   
   The API Url,Input and Ouptut can be seen in the image
   ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/f38a8201-8152-46c8-8190-c2dbe46b15e6)

   Scenario 3:
   The api will return status code - 400 if data is not provided correctly and 500 if database error

3. Method - DELETE:

   1. Source Code Function - delete_toy(toy_id)
      
      Scenario 1:
      The above method and fucntion will delete the toy with the Toy ID, will return the output and status code - 200
      
      The API Url,Input and Ouptut can be seen in the image
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/f5e6c6d4-c3cf-4c8d-86bb-bef17580e3a3)
      
      Scenario 2:
      If the toy doesn't exists with ID while deletion, it will return the below output and status code - 404
      
      The API Url,Input and Ouptut can be seen in the image
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/e55778e2-1b63-45ed-a1c7-a0e6c3b73965)

      Scenario 3:
      The api will return status code - 500 if  database error

   2. Source Code Fucntion - delete_all_toys()
      
      The above menthod and function will clear all the records in SQL Database, will return the below output and status code -200
      
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/746afda8-d4eb-4da0-817b-7a4c0b6ad4ca)

      The api will return status code - 500 if  database error

4. Method - GET:
   
   1. Source Code Function - get_toys()

      Scenario 1:
      The above method and fucntion will fetch all the data of toys in database, will return the output and status code - 200
      
      Pagenation is added to this EndPoint, to run the api two params need to created as below, if params are not added, by default page will be 1 and no.of items will be 10
      1. page(page number)
      2. per_page(items per page)

      The API Url,Input and Ouptut can be seen in the image
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/b8415bdf-1dcd-48a6-a0ed-749321e5a6e5)
      
      Scenario 2:
      The api will return status code - 500 if database error

   3. Source Code Function - get_toy(toy_id)

      Scenario 1:
      The above method and fucntion will fetch the toy with the Toy ID, will return the output and status code - 200
      
      The API Url,Input and Ouptut can be seen in the image
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/66ad3a3f-4564-4012-9d09-fdff113b7807)

      Scenario 2:
      If the toy doesn't exists with ID while fetching, it will return the below output and status code - 404
      
      The API Url,Input and Ouptut can be seen in the image
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/e27e3435-9cc0-4bbd-810d-0b9896ee5162)

      Scenario 3:
      The api will return status code - 500 if database error

   5. Source Code Function - search_toy()

      Scenario 1:
      The above method and function will fetch the toys by searching with the Name of the toy, if found wil return the result with status code - 200
      
      The API Url,Input and Ouptut can be seen in the image
      
      Need to add a Param as below
      1. Name(name of the toy partial name or full name)
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/be2081a9-44fc-48f7-bf65-c99648901ddb)

      Scenario 2:
      If the api does't not find any toy with the search name it will return the below displayed message with status code - 404
      
      The API Url,Input and Ouptut can be seen in the image
      ![image](https://github.com/ajithganthala/flask_api_project/assets/58483240/05efab0c-eac0-42ea-8800-c96d9f172df1)

      Scenario 3:
      The api will return status code - 500 if database error

**The above information and scenarios will cover all - installations, usage, and test cases as well**

**If any support please fell free to reach out to me**

**Thank You Enjoy the Project**



      

      
   



   




