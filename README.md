# ITNE352-Project---GroupSA12---2nd Semester 2024\2025

### Title: Flights Multithreaded Server-Client System
 
 Name: Mohammed Abdulsalam &nbsp;
 ID: 202210939 &nbsp;
 Section: 1

Table of Contents:
1. Script Requirements
2. Run the Scripts
3. Script Description
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
