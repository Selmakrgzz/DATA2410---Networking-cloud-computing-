import socket
import threading
import sys  # In order to terminate the program

def handle_client(client_socket, addr):
    print(f"Connection from {addr}")
    
    #Receiving the message from the client side
    message = client_socket.recv(1024).decode()

    #Extracting the filename
    filename = message.split()[1]

    try:
        #Opening the file
        with open(filename[1:], 'r') as f:
            #Reading the file to be sent back to client
            outputdata = f.read()
            print(filename)

            #Sending one HTTP header line into socket
            #Also sending the output data to the client
            http_response = f"HTTP/1.1 200 OK\r\n\r\n {outputdata}"
           
            # Send HTTP-responsen til klienten
            client_socket.send(http_response.encode())

            # Send innholdet i den forespurte filen til klienten
            client_socket.sendall(outputdata.encode())
    except FileNotFoundError:
        #Sending response message for file not found
        http_response = "HTTP/1.1 404 Not Found\r\n\r\nFile Not Found"
        
        client_socket.send(http_response.encode())

    # Close client socket
    client_socket.close()


def main():
    # Create a socket called serverSocket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Prepare a sever socket
    server_port = 7888
    server_ip = '127.0.0.1'

    # Establishes a connection between the server's IP address and the specified port number
    serverSocket.bind((server_ip, server_port))
    # Waiting for a connection
    serverSocket.listen(5)
    print('The server is ready to receive')

    while True:
        # Establish the connection print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        print(f"Connection established from {addr}")

        # Handle client in a new thread
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket, addr))
        client_thread.start()

        #If the client dosen't connect again, thw while will turn false and server will close
        if not handle_client:
            break
    
    serverSocket.close()
    sys.exit()#Terminate the program after sending the corresponding data



if __name__ == '__main__':
    main()
