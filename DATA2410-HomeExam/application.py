import argparse
import sys
from struct import *
from socket import *
import _thread as thread

#Checking the struct offical page I found out
#that I will have to use HHH which is equal
#to 6 bytes: 3 unsigned shorts (2 bytes each)
header_format = 'HHH' 

#Checking if the header_format does equal to 6
#print(f'header size: {calcsize(header_format)}')

def create_packet(header_format, seq, ack, flags, data):
    #Creating a package with header information and application data
    #Input arguments are; sequence number, acknowledement number,
    #flags(only 4 bits) and application data
    #The header values will be packed according to the header_format HHH
    header = pack(header_format, seq, ack, flags)

    #Once the header is created, we add the application data
    #The application data is on 994 bytes and the header 6 bytes = 1000 bytes
    packet = header + data

    #Showing the length of the package
    print (f'packet containing header + data of size {len(packet)}')
    return packet

#I will be managing the packet making here
def packaging(seq, ack, flags, data):
    #Creating packet with sequence number 1
    print('\n\ncreating a packet')

    print(f'App data for size={len(data)}')

    #msg will now hold a packet which includes our custom header and data
    msg = create_packet(header_format, seq, ack, flags, data)

    return msg

def client(IP, Port, data):
    #Creating a socket called "clientSocket"
    #AF_INET indicates that the underlying network is using IPv4
    #DGRAM indicates that it is a UDP socket
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    sequence_number = 1
    acknowledgement_number = 0
    #We will not set any flags when we send a data packet
    flags = 0

    #Checking the connection
    try:
        #Connect to the server
        clientSocket.connect((IP,Port))
        print("Connection established successfully")
    except:
        print("Connection error")
        sys.exit()
    
    #Receiving the package
    packet = packaging(acknowledgement_number, sequence_number, flags, data)
    #Sending the package to the server side
    clientSocket.sendall(packet.encode())
    #Requesting the server response
    response = clientSocket.recv(1024)
    print(f"Server response: {response.decode()}")

    clientSocket.close()

def parse_header(header):
    #A header og 6 bytes are taken as an argument
    #Unpacking the value based on the specific header format given
    #Returning the values as a tuple
    header_from_msg = unpack(header_format, header)
    
    return header_from_msg

def parse_flags(flags):
    #Parsing only the first 3 fields
    #since we won't be using the last one rst
    syn = flags & (1 << 3)
    ack = flags & (1 << 2)
    fin = flags & (1 << 1)
    return syn, ack, fin

def server(IP, Port):
    #Defining a function to handle client connections
    def handleClient(connection, addr):
        #Printing a message to indicate that a connection has been accepted
        print(f"Accepted connection from {addr}")
        
        #Looping to continuously receive data from the client
        while True:
            #Receiving data from the client (up to 1024 bytes) and decode it
            received_line = connection.recv(1024).decode()

            #KAN FJERNE DENNE EVT
            #Check if the received data is "exit"
            if  received_line == "exit":
                break
            else:
                #If data received is not "exit"
                print(f"Received equation: {received_line}")

                #Read data from the client and print
                result = package

                #Send data back over the connection
                connection.send(result.encode())

        # Close the connection with the client
        connection.close()
        print(f"Connection with {addr} closed")

    #Create a socket called "serverSocket" using UDP
    serverSocket = socket(AF_INET,SOCK_DGRAM)

    try:
        #Bind the server socket
        serverSocket.bind((IP,Port))
    except: 
        print("Bind failed. Error : ")
        sys.exit()

    #Telling the user that the server is listening on given ip and port
    print(f"Server listening on {IP} :{Port}")

    #Activating listening on the socket
    serverSocket.listen(1)

    #Telling the user that the server is waiting for a connection
    print("Waiting for connections...")

    #Im using multithreading because this assignment involves implementing
    #a reliable data transfer protocol over UDP using GBN, it is beneficial
    #when sending and receiving data packets, sliding window, handling timeout etc...
    while True:
        #Server waits on accept() for connections
        connectionSocket, addr = serverSocket.accept() 

        #Telling the user that the server has made a connection
        print(f"New connection from {addr}") 
        thread.start_new_thread(handleClient, (connectionSocket, addr))
        
        if not handleClient:
            break
    serverSocket.close()

#Method to check the given port
def checkPort(port):
    if 1025 <= port <= 65535: #Checking the given interval
        return True
    else:
        return False

#Method to check the range of given IP address
def checkRangeIP(IP):
    num='' #Setting the num to be a string since we will add the belonging digits and not sum them
    result=True #Setting the result to true by defualt
    for i in IP: #Iterating through the given IP address
        if i.isdigit(): #Selecting out the digits
            num=num+str(i) #Appending the digits
        elif i == '.': #When we come to the end of each block in the IP address
            intNum=int(num) #Parsin the string to an int
            num='' #Emtying the num for later use
            if 0 <= intNum <= 255: #Checking the given interval for each block
                continue #If true, continue
            else:
                result=False #If not true, then update result to be false
                break #And break out
    if num: #If num is not emty, which will be the last block in the IP address
        intNum=int(num) #Parsing the string to int
        if not(0 <= intNum <= 255): #Checking the given interval for each block
            result = False

    return result #Returning the result as a boolean
    
#Method to check if the given IP address is submitted with the right format AKA having 3 dots
def checkDot(IP):
    if IP.count('.') == 3: #Counting the dots to be equeal to 3
        return True
    else:
        return False

#Just a basic argumentline checker that will make sure that the user don't use a invalid port number og ip-adress.
#It gives informative feedback so the user can make sure to type in the correct format
def argumentlineCheck(mode, IP, Port):
    if Port and IP and checkPort(Port) and checkRangeIP(IP) and checkDot(IP):
        print(f"Output: The {mode} is running with IP address = {IP} and port address = {Port}")
    elif not checkDot(IP):
        print(f"Output: Invalid IP. It must be in the format: 10.1.2.3")
    elif not checkRangeIP(IP):
        print(f"Output: IP blocks must be within [0, 255]")
    elif not checkPort(Port):
        print(f"Output: Invalid port. It must be within range [1024, 65535]")

def fileHandling(filename):
    #To handle the jpeg file we'll open the file in
    #binary mode rb, read the data and return them
    #as a bytes string which will be sent over the
    #DRTP/UDP conncetion to the server
    with open(filename, 'rb') as f:
        outputdata = f.read()
    return outputdata

def main ():
    parser = argparse.ArgumentParser(description='transfer-server/client')

    parser.add_argument('-s', '--server', action='store_true', help="Invoke as the server")
    parser.add_argument('-c', '--client', action='store_true', help="Invoke as the client")
    parser.add_argument('-f', '--file', nargs='?', help='Enter the filename')
    parser.add_argument('-i', '--serverIP', help='Enter the server IP')
    parser.add_argument('-p', '--serverPort', type=int, help='Enter the server port number')

    args = parser.parse_args()
    
    if args.server:
        print('connected to server')
    elif args.client:
        print('connected to client')

    #Checking the argumentline if the given ip and port is valid,
    #if the user uses both client and server at the same time or
    #dosen't define any of them
    if args.server:
        argumentlineCheck('server', args.serverIP, args.serverPort)
        #If the argumentline get's through the check then we can connect
        if argumentlineCheck():
            server(args.serverIP, args.serverPort)
        else:
            print('Couldnt connect to server due to missing/wrong arguments')
    elif args.client:
        argumentlineCheck('client', args.serverIP, args.serverPort)
        #If the argumentline get's through the check then we can connect
        if argumentlineCheck:
            outputdata = ""
            #Checking if the user have specified any file
            if args.file == None:
                print('No file specified')
            else: 
                print(f'File {args.file} specified')
                outputdata = fileHandling()
            #Sending the IP, Port and the given jpeg file
            #as a bytes string to the client to handle
            client(args.serverIP, args.serverPort, outputdata)
        else:
            print('Couldnt connect to client due to missing/wrong arguments')
    elif args.server & args.client:
        print('Output: You cannot use both at the same')
    elif len(sys.argv) == 1:
        print('Output: You should run either in server or client mode')


    


if __name__ == '__main__':
    main()



#DU SKAL HÅNDTERE PAKKEN SOM BLIR MOTATT AV SERVEREN