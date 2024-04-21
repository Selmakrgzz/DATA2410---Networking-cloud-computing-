#TASK1
Starting the server first and then load the client web browser with the given url. Client requests a specific file, index.html from the server. The server extracts the filename and opens it up to be readable. The client side will get a http response that the process is OK. The data in the index.file will be iterated through a for loop and sent to the client web browser. There are also a error handling part of the code that make sure to give a suitable http response directly back to the client web browser.


#TASK2
Using argsparse to get the ip, port and requested filename from client. Creating a socket that's using TCP. Handling errors with try/exception. Checking the connection between server and client. Using the input from argparse to send a HTTP GET request to server. We will receive the http 200 OK in client if the process has completed as it should.


#TASK3
The server handles now multiple http requests now by implementing multithreded server. Created a function handle_client that will handle each client from the new request. Other than that it's mostly the same as the other tasks.

#...Note

For the task 2 and 3 I have only used clientSocket.sendall(outputdata.encode()) and not the for-loop method as given in the shell code because I encountered some errors and dificulties.