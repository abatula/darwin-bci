import socket
import struct

#clientAddr = '192.168.123.1' # Address of the machine receiving commands
clientAddr = ''
clientPort = 60000

tmp = input('Press enter when ready to connect')

# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((clientAddr, clientPort))
s.listen(1)
clientSock, addr = s.accept()

sendChar = None
while sendChar != '0':
    sendChar = input('Enter command [1-4] or 0 to quit: ')
    if sendChar in '01234':
        msg = struct.pack('<h', int(sendChar))
        clientSock.sendall(msg)
    else:
        print('Invalid character')