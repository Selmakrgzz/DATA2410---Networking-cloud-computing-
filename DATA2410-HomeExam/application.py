import argparse
import sys

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

def main ():
    parser = argparse.ArgumentParser(description='transfer-server/client')

    parser.add_argument('-s', '--server', action='store_true', help="Invoke as the server")
    parser.add_argument('-c', '--client', action='store_true', help="Invoke as the client")
    parser.add_argument('-f', '--file', nargs='?', help='Enter the filename')
    parser.add_argument('-i', '--serverIP', help='Enter the server IP')
    parser.add_argument('-p', '--serverPort', help='Enter the server port number')

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
    elif args.client:
        argumentlineCheck('client', args.serverIP, args.serverPort)
    elif args.server & args.client:
        print('Output: You cannot use both at the same')
    elif len(sys.argv) == 1:
        print('Output: You should run either in server or client mode')


if __name__ == '__main__':
    main()