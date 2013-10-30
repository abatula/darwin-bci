from __future__ import print_function, division

import time
import sys
import socket
import struct

sys.path.append('../MotionController') 

import MotionController

WALK_FORWARD_TIME = 3
WALK_BACKWARD_TIME = 4
WALK_STEP_SIZE = 10
TURN_TIME = 3
TURN_STEP_SIZE = 0

END_PROGRAM_VAL = 0

programRunning = False
#serverAddr = '172.17.101.2' # Address of the machine sending commands
serverAddr = '192.168.123.105' # Address of the machine sending commands
serverPort = 60000

socketConnected = False

def SetupConnection(sock=None):
    """ 
    Set up TCP/IP communication
    
    INPUT:
        sock    - Socket object for TCP/IP communication (default None)
        
    OUTPUT:
        sock    - Socket object for TCP/IP communication 
        socketConnected - Whether the socket was successfully connected (boolean)
    """
    if sock == None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    sock.setblocking(1)
    
    try:
        sock.connect((serverAddr,serverPort))
        socketConnected = True
    except socket.error:
        socketConnected = False
        print('ERROR: Socket connection refused')
        
    return dict(sock=sock, socketConnected=socketConnected)
        
def ReadData(sock, numBytes, fmt='-'):
    """ 
    Read and return data from TCP-IP and log it as debug info 
    
    INPUT:
        sock - socket to receive dataChunkFolder
        fmt - unpack format or '-' for do not unpack
    OUTPUT:
        buff - Unconverted received buffer
        data - Converted data (None if unpack failed)
    """
    
    data = None
    
    try:
        buff = sock.recv(numBytes)
    except socket.timeout:
        buff = None
        data = None
        
    if fmt == '-': # Do not unpack if format is '-'
        data = buff
    elif buff is not None: # Only unpack if format is not '-' and buffer read successfully
        if len(buff) == numBytes: # If not enough data was read, do not try to unpack
            try:
                data = struct.unpack_from(fmt, buff)[0]
            except:
                data = None
    return data
        
def MoveForward(controller):
    "Walk forward one tile length"
    controller.walk(WALK_FORWARD_TIME, 0, WALK_STEP_SIZE)
    
def MoveBackward(controller):
    " Walk backward one tile length"
    controller.walk(WALK_BACKWARD_TIME, 0, -WALK_STEP_SIZE)
    
def TurnRight(controller):
    "Turn 90 degress to the right"
    controller.walk(TURN_TIME, -25, TURN_STEP_SIZE)
    
def TurnLeft(controller):
    "Turn 90 degrees to the left"
    controller.walk(TURN_TIME, 14, TURN_STEP_SIZE)

controller = MotionController.PyMotionController()

initialized = False

try:
    initialized = controller.initMotionManager()
except:
    print('\nException occured')

if initialized:
    print("Initialized")
    controller.initActionEditor()
            
    controller.initWalking()
    tmp = raw_input('continue: ')
    
    # Connect to the socket
    socketInfo = SetupConnection()
    sock = socketInfo['sock']
    socketConnected = socketInfo['socketConnected']
    
    if socketConnected:
        print('Socket Connected')
        programRunning = True
    
        # Wait for command before moving
        while programRunning:
            cmd = ReadData(sock, 2, '<h')
            if cmd == None:
                pass
            else:
                print('Received command ' + str(cmd))
            if cmd == END_PROGRAM_VAL:
                programRunning = False
                break
            # Numbers are in the same order as the commands for the BCI (RH, LH, LF, RF)
            elif cmd == 1:
                TurnRight(controller)
            elif cmd == 2:
                TurnLeft(controller)
            elif cmd == 3:
                MoveForward(controller)
            elif cmd == 4:
                MoveBackward(controller)

    time.sleep(1)
    
    controller.initActionEditor()
    controller.executePage(15)
    
    while controller.actionRunning():
        time.sleep(0.5)
else:
    print('Initialization Failed')
