from __future__ import print_function, division

import time

import sys

sys.path.append('../MotionController') 

import MotionController

def MoveForward(controller):
    "Walk forward one tile length"
    controller.walk(5, 0, 10)
    
def MoveBackward(controller):
    " Walk backward one tile length"
    controller.walk(5, 0, -10)
    
def TurnRight(controller):
    "Turn 90 degress to the right"
    controller.walk(5, -10, 10)
    
def TurnLeft(controller):
    "Turn 90 degrees to the left"
    controller.walk(5, 10, 10)

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
    time.sleep(1)
    
    MoveForward(controller)
    
    MoveBackward(controller)
    
    TurnRight(controller)
    
    TurnLeft(controller)
    
    controller.initActionEditor()
    controller.executePage(15)
    
    while controller.actionRunning():
        time.sleep(0.5)
else:
    print('Initialization Failed')
