import socket
import struct

#clientAddr = '192..168.123.1' # Address of the machine receiving commands
clientPort = 60000

tmp = input('Press enter when ready to connect')

# Create the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((clientAddr, clientPort))
s.listen(10)
clientSock, addr = s.accept()

sendChar = None
while sendChar != '0':
    sendChar = input('Enter command [1-4] or 0 to quit: ')
    msg = struct.pack(sendChar, '<c')
    clientSock.sendall(msg)