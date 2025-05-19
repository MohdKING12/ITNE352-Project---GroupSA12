# ITNE352-Project---GroupSA12---2nd Semester 2024\2025

### Title: Flights Multithreaded Server-Client System
 
 Name: Mohammed Abdulsalam &nbsp;
 ID: 202210939 &nbsp;
 Section: 1

Table of Contents:
1. Script Requirements
2. Run the Scripts
3. Scripts Description
4. Additional Concept
5. Acknowledgments
6. Conclusion

<br><br><br>

> Script Requirements:
<br>
For this project, I used a handful of libraries to get an excellent and fault tolerant environment. (Note: this script is designed for python version 3 and above, make sure you have it downloaded at latest version )

<br><br>

* Request library : 
    * This library uses HTTP protocol to get or post data to a website. In this project, it is use to fetch the data from the API, getting all needed information to make the server handle the clients requests.

    * This library must be downloaded first as it is not built-in python library. Using this command in the command prompt will download it: 
__pip3 install requests__ 

    * This command will ensure to download the library for python3, which is the most modern.

* JSON library:
For this library, it is used to extract the data in JSON format. This allows to organize the output that will be shown for the client. This library is built-in python library, so there should be no installation required.

* Socket library:
It is used to create sockets for clients and the server so the can communicate through. This library is built-in python library, so there should be no installation required.

* Threading library:
It allows the socket to handle multiple communications simultaneously. This is the main idea for this project. This library is built-in python library, so there should be no installation required.

* Time library:
Not much included within script, but it is crucial. As I will illustrate later, I used __time.sleep()__ function to make server handle the first input from the user and not to mix up with the next input. This library is built-in python library, so there should be no installation required.
<br>
These are all the libraries that are going to be used to run the scripts. Only request library needs to be downloaded, the other ones are built-in libraries. 
If, for any reason, one of these libraries are not already downloaded just run this command in your command prompt followed by the library name to install it:

**pip3 install** (name of the library in lowercase. [e.g. threading])
<br><br><br>


> Run Scripts:

After making sure all libraries are successfully installed, take the scripts and place them in the same folder. If any of the scripts are not inside the same folder as the rest of the scripts, then the whole system will not work, as they depend on each other.

1.	Then you must run the server script first, so it will go passive and start listening for any incoming requests from clients. You can run in your code editor or using your device command prompt. **(Steps for running in command prompt are illustrated down)**

2. In command prompt, you will run the interface script, where you can communicate with the server through. 
    * First make sure to enter the folder that saved the scripts inside. Using the file explorer go to the folder location, then you can find the path at the top **(Blue Circle)**. 
    * Press on the empty space **(Red DOT in picture)** inside the location panel and copy it
    ![Alt text](pictures/Capture.PNG)

3. In the command prompt, type: **cd (paste the path)** then press enter. 
    * Now you are inside the folder, to run the interface script type: **python3 interface_module.py** then press enter.
    * If it did not work, try : **python interface_module.py**.

4. At the beginning, it will ask for your name then the ICAO for the airport you want to get information about.

5. After that you can easily interact with the server via menu of options for server to execute. Only enter the number of the service you want ( 1-4) and the server will handle everything for you and return the desired information, if there is any.

<br><br>



> Scripts Descriptions:
1.	API script [ api.py]:
This script includes functions that are going to be used for fetching data from the **aviation.com** API, saving data in a JSON file, and retrieve data from the file based on client prompt.


| Main Functions    | Description     |
|-------------|--------------|
| `save_to_file(data, filename='group_SA12.json')` |It takes two parameters **data** which is the fetched data from  **aviation.com** API & **filename** is the name of the file that data will be saved inside, and it is always '**group_SA12.json**'. This function stores the data to a file, so server can retreive data from it.  |
| `get_flights_by_airport_code(icao_code)`     |Takes one parameter, which is **icao_code** of the airport that data will be fetched about. The function uses **request** library to get the data of the airport, and return the data it gets ( if there are any).  | 
| `get_arrived_flights(data)` |Takes the **data** of the airport, and returns list of dictionary details about flights that arrived at the airport|
| `get_delayed_flights(data)` |Takes the **data** of the airport, and returns list of dictionary details about flights that are delayed|
| `get_flight_details(iata_code)` |This function takes the **iata_code** of the flight, and then fetch data related to it from **aviation.com** API. It returns a dictionary of details about the flight|


| Subfunction          | Description     |
|---------------------|--------------------|
| `json.dump(data, f, indent=4)`|This function from **json** saves the data in JSON format. I give it three parameters **data** fetched, **f** is the file name,and **indent** is the indentation inside the file to orgnize it  |
| `requests.get(BASE_URL, params)`              |This function from **request** library sends a HTTP GET request. Takes the **BASE_URL** which is the URL of the website, and **params** it has to be predefined and contains extra information for the path like the access key of **API** and **ICAO code** |
| `.get()`|It is a safe way to retrieve data and not raising an error or exception|
