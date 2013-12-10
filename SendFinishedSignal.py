# Send finished signal to the main BCI program
# This should be run from the experiment computer used to control DARwIn-OP

import socket

serverAddr = '192.168.0.105' # Address to communicate with
serverPort = 60001

msg = b'F' + b'\x00'

sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up socket connection
try:
    sock.connect((serverAddr, serverPort))
except socket.error:
    print('ERROR: Socket connection refused')
else:
    print('Connected\n')
    
    sendData = True
    
    while sendData:
        inputChar = input('Enter 1 to end or 0 to quit: ')
        if inputChar == '0':
            sendData = False
        else:
            sock.sendall(msg)
            
    sock.close()