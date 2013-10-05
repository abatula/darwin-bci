from __future__ import print_function, division

import time

import sys

sys.path.append('../MotionController') 

import MotionController

WALK_FORWARD_TIME = 3
WALK_BACKWARD_TIME = 4
WALK_STEP_SIZE = 10
TURN_TIME = 3
TURN_STEP_SIZE = 0

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
    
    for i in range(5):
        MoveForward(controller)
        time.sleep(1)
     
    tmp = raw_input('continue: ') 
     
    for i in range(5):
        MoveBackward(controller)
        time.sleep(1)
    
    #MoveForward(controller)
    
    #tmp = raw_input('continue: ')
    
    #MoveBackward(controller)
    
    #tmp = raw_input('continue: ')
    
    #TurnRight(controller)
    
    #tmp = raw_input('continue: ')
    
    #TurnLeft(controller)
    
    time.sleep(1)
    
    controller.initActionEditor()
    controller.executePage(15)
    
    while controller.actionRunning():
        time.sleep(0.5)
else:
    print('Initialization Failed')
