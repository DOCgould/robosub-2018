import time
import socket
import PyQt4.QtCore
import movement
import Missions
from PyQt4 import QtCore
import joystick_controller
import copy
import lib.Utils.utilities as utilities

class MissionPlanner(QtCore.QThread):
    
    '''
    MissionPlanner class will controll what missions we need to do and in what order
    It will send data to the control systems module which will get us to a specific waypoint
    It will also recieve data from the computer vision comm as to where 
    '''
    
    def __init__(self, externalCommClass):
        QtCore.QObject.__init__(self)
        self.missionList = []
        self.currentMission = None
        self.changeMission = None
        self.changeFlag = None
        self.running = False
        
        self.externalCommClass = externalCommClass
        self.externalCommThread = self.externalCommClass.externalCommThread
        self.maestroSerial = None

        self.debug = True
        self.manualMode = False
        
        self.joystickController = None
        
        self.missionCommander = None
        self.controlSystemClass = None
        
        '''
        mission Debug Boolean; The difference between the two is that 'missionDebug' is used when trying to debug mission
                where as 'debug' is used when the sub isn't in the water
        '''
        self.missionDebug = False
        
        self.thrusters = []
#         self.thrusters.append(movement.BrushedThruster(1, [0, 0, 0], [-1, 0, -1]))#Up/Down thruster
#         self.thrusters.append(movement.BrushedThruster(2, [1, 0, 0], [0, 1, 0]))  #Up/Down thruster
#         self.thrusters.append(movement.BrushedThruster(3, [0, 0, 0], [-1, 0, 1]))  #Up/Down thruster
#         self.thrusters.append(movement.BrushedThruster(4, [0, 0, 1], [0, -1, 0]))  #Up/Down thruster
#         self.thrusters.append(movement.BrushedThruster(5, [0, 0, 0], [1, 0, 1])) #Left/Right thruster
#         self.thrusters.append(movement.BrushedThruster(6, [1, 0, 0], [0, -1, 0])) #Left/Right thruster
#         self.thrusters.append(movement.BrushedThruster(7, [0, 0, 0], [1, 0, -1])) #Fwd/Rev thruster
#         self.thrusters.append(movement.BrushedThruster(8, [0, 0, 1], [0, 1, 0])) #Fwd/Rev thruster
        
        #some of these are backwards because thrusters were plugged in incorrectly, numbers 3,4,7,8
        self.thrusters.append(movement.BrushedThruster(1, [0, 1, 0], [-1, 0, 1]))
        self.thrusters.append(movement.BrushedThruster(2, [-1, 0, 0], [0, 0, 1]))  
        self.thrusters.append(movement.BrushedThruster(3, [0, 1, 0], [1, 0, 1]))  
        self.thrusters.append(movement.BrushedThruster(4, [0, 0, -1], [1, 0, 0])) 
        self.thrusters.append(movement.BrushedThruster(5, [0, 1, 0], [1, 0, -1])) 
        self.thrusters.append(movement.BrushedThruster(6, [-1, 0, 0], [0, 0, -1])) 
        self.thrusters.append(movement.BrushedThruster(7, [0, 1, 0], [-1, 0, -1]))
        self.thrusters.append(movement.BrushedThruster(8, [0, 0, -1], [-1, 0, 0])) 
        
        #PID values - These values are can be changed by the "changePIDValues" function and will change the values in movement.py
        self.autonomousPIDs = []
        self.manualPIDs = []
        
        self.yawAutonomousPIDControllerForwardModeValues = [0,0,0,0,0,0]
        self.yawAutonomousPIDControllerBackwardsModeValues = [0,0,0,0,0,0]
        self.pitchAutonomousPIDControllerValues = [0,0,0,0,0,0]
        self.rollAutonomousPIDControllerValues = [0,0,0,0,0,0]
        self.depthAutonomousPIDControllerValues = [0,0,0,0,0,0]
        self.xAutonomousPIDControllerValues = [0,0,0,0,0,0]
        self.zAutonomousPIDControllerValues = [0,0,0,0,0,0]
        
        self.yawManualPIDControllerForwardModeValues = [0,0,0,0,0,0]
        self.yawManualPIDControllerBackwardsModeValues = [0,0,0,0,0,0]
        self.pitchManualPIDControllerValues = [0,0,0,0,0,0]
        self.rollManualPIDControllerValues = [0,0,0,0,0,0]
        self.depthManualPIDControllerValues = [0,0,0,0,0,0]
        self.xManualPIDControllerValues = [0,0,0,0,0,0]
        self.zManualPIDControllerValues = [0,0,0,0,0,0]
        
        self.yawAutonomousPIDControllerForwardMode = movement.PIDController(*self.yawAutonomousPIDControllerForwardModeValues)
        self.yawAutonomousPIDControllerBackwardsMode = movement.PIDController(*self.yawAutonomousPIDControllerBackwardsModeValues)
        self.pitchAutonomousPIDController = movement.PIDController(*self.pitchAutonomousPIDControllerValues)
        self.rollAutonomousPIDController = movement.PIDController(*self.rollAutonomousPIDControllerValues)
        self.depthAutonomousPIDController = movement.PIDController(*self.depthAutonomousPIDControllerValues)
        self.xAutonomousPIDController = movement.PIDController(*self.xAutonomousPIDControllerValues)
        self.zAutonomousPIDController = movement.PIDController(*self.zAutonomousPIDControllerValues)
        
        self.autonomousPIDs.append(self.yawAutonomousPIDControllerForwardMode)
        self.autonomousPIDs.append(self.yawAutonomousPIDControllerBackwardsMode)
        self.autonomousPIDs.append(self.pitchAutonomousPIDController)
        self.autonomousPIDs.append(self.rollAutonomousPIDController)
        self.autonomousPIDs.append(self.depthAutonomousPIDController)
        self.autonomousPIDs.append(self.xAutonomousPIDController)
        self.autonomousPIDs.append(self.zAutonomousPIDController)
        
        self.yawManualPIDControllerForwardMode = movement.PIDController(*self.yawManualPIDControllerForwardModeValues)
        self.yawManualPIDControllerBackwardsMode = movement.PIDController(*self.yawManualPIDControllerBackwardsModeValues)
        self.pitchManualPIDController = movement.PIDController(*self.pitchManualPIDControllerValues)
        self.rollManualPIDController = movement.PIDController(*self.rollManualPIDControllerValues)
        self.depthManualPIDController = movement.PIDController(*self.depthManualPIDControllerValues)
        self.xManualPIDController = movement.PIDController(*self.xManualPIDControllerValues)
        self.zManualPIDController = movement.PIDController(*self.zManualPIDControllerValues)
        
        self.manualPIDs.append(self.yawManualPIDControllerForwardMode)
        self.manualPIDs.append(self.yawManualPIDControllerBackwardsMode)
        self.manualPIDs.append(self.pitchManualPIDController)
        self.manualPIDs.append(self.rollManualPIDController)
        self.manualPIDs.append(self.depthAutonomousPIDController)
        self.manualPIDs.append(self.xManualPIDController)
        self.manualPIDs.append(self.zManualPIDController)
        
        
        #This controls which control system the sub uses to move around in autonomous mode. Its either
        #the autonmous movement, joystick movement, or state space based
        self.MovementController = None
        self.relativeMoveWaypoint = None
        
    #Allows Mission Planner to access Mission Commander so that they can communicate together
    def setReferences(self, missionC, controlSystem):
        self.missionCommander = missionC
        self.controlSystemClass = controlSystem
        labelNames = ["Kp", "Ki", "Kd", "Controller", "Integration Min", "Integration Max"]
        tabLayoutNames = ["YawForward", "YawBackward", "Pitch", "Roll", "Depth", "XPosition", "ZPosition"]
        values = []
        for i,v in enumerate(tabLayoutNames):
            inVal = []
            for n,p in enumerate(labelNames):
                inVal.append(self.controlSystemClass.PIDVals[v+"_"+p])
            values.append(inVal)
        self.changePIDValues(False, values)
        
    #Sets the mission List, only called right before starting the sub in debug mode or actual mode
    def setMissionList(self, missionList):
        self.missionList = missionList
        
        
    def connectSignals(self):
        self.connect(self.missionCommander, QtCore.SIGNAL("setDebugMissionMode(PyQt_PyObject)"), self.setDebugMissionMode)
        self.connect(self.missionCommander, QtCore.SIGNAL("nextOrPreviousFlag(PyQt_PyObject)"), self.nextOrPreviousFlag)
        self.connect(self.missionCommander, QtCore.SIGNAL("nextOrPreviousMission(PyQt_PyObject)"), self.nextOrPreviousMission)
        self.connect(self.controlSystemClass, QtCore.SIGNAL("updatePIDValues(PyQt_PyObject)"), lambda val: self.changePIDValues(False, val))
        self.connect(self.externalCommClass, QtCore.SIGNAL("stopThread"), self.stopThread)
        self.connect(self.externalCommClass, QtCore.SIGNAL("waypointChanged(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"), lambda val1, val2, val3: self.changeWaypoint(val1, val2, val3))
        
        for i,v in enumerate(self.missionList):
            self.connect(v, QtCore.SIGNAL("debugMessage(PyQt_PyObject)"), self.sendDebugMessage)
    
    #Changes the Mission Debug Value on the Fly
    def setDebugMissionMode(self, value):
        self.missionDebug = False
    
    def nextOrPreviousFlag(self, next):
        self.changeFlag = next
    
    def nextOrPreviousMission(self, next):
        self.changeMission = next
    
    def sendDebugMessage(self, string):
        self.emit(QtCore.SIGNAL("missionDebugMessage(PyQt_PyObject)"), string)
    
    def startManualControl(self):
        self.manualMode = True
        self.debug = False
        self.maestroSerial = self.externalCommThread.maestroSerial
        self.joystickController = joystick_controller.controllerResponse()
        self.joystickController.start()
        if self.externalCommThread.dvlResponseThread != None:
            self.externalCommThread.dvlResponseThread.clearDistanceTraveled()
        self.MovementController = movement.JoystickMovementController(self.maestroSerial, self.manualPIDs, self.thrusters[0],self.thrusters[1],self.thrusters[2],self.thrusters[3],self.thrusters[4],self.thrusters[5],self.thrusters[6],self.thrusters[7])
        print "Starting Manual Control..."
        self.start()
        
    def stopManualControl(self):
        self.manualMode = False
        self.running = False
        self.joystickController.killThread()
        print "Stopping Manual Control..."
        
        
    
    #Starts the thread for autonomous run, in case the gui crashes this will still continue
    def startAutonomousRun(self, debug):
        self.debug = debug
        self.running = True
        self.manualMode = False
        self.maestroSerial = self.externalCommThread.maestroSerial
        #Creates the movement controller for autonomous mode, parameters are null since we don't have the TCB's yet
        if self.debug == False:
            self.MovementController = movement.MovementController(self.maestroSerial, self.autonomousPIDs, self.thrusters[0],self.thrusters[1],self.thrusters[2],self.thrusters[3],self.thrusters[4],self.thrusters[5],self.thrusters[6],self.thrusters[7])
            if self.externalCommThread.dvlResponseThread != None:
                self.externalCommThread.dvlResponseThread.clearDistanceTraveled()
            else:
                print "No DVL Connected"
        if not "missionList" in self.externalCommThread.guiData:
            print "No missions in \"missionList\"... Not starting"
            return
        self.missionList = self.externalCommThread.guiData["missionList"]
        self.start()
        
    def stopAutonomousRun(self):
        self.running = False
        
    #Returns the current mission.... Usefull for Nate and his Map for some reason
    def getCurrentMission(self):
        self.emit(QtCore.SIGNAL("currentMission(PyQt_PyObject)"), self.currentMission)
        
    #Change Waypoint - Allows for us to change the General Waypoint of a Mission while the sub is in the water
    def changeWaypoint(self, missionName, waypointPosition, waypointOrientation):
        print "Waypoint Changed"
        if missionName in self.missionList:
            self.missionList[missionName].generalWaypoint = waypointPosition + waypointOrientation
            #print "Waypoint changed to " + str(waypointPosition + waypointOrientation)
    
    #Function is connected to the control system widget. Updates the PID values when the sliders change
    #ManualPIDs is a boolean. If its true then the PIDs are for manual mode, else they are for Autonomous Mode
    def changePIDValues(self, manualPIDs, values):
        if len(values) < 7:
            return
        if manualPIDs == True:
            self.yawManualPIDControllerForwardModeValues = values[0]
            self.yawManualPIDControllerBackwardsModeValues = values[1]
            self.pitchManualPIDControllerValues = values[2]
            self.rollManualPIDControllerValues = values[3]
            self.depthManualPIDControllerValues = values[4]
            
        
            self.xManualPIDControllerValues = values[5]
            self.zManualPIDControllerValues = values[6]
            
            self.yawManualPIDControllerForwardMode.changePIDs(*self.yawManualPIDControllerForwardModeValues)
            self.yawManualPIDControllerBackwardsMode.changePIDs(*self.yawManualPIDControllerBackwardsModeValues)
            self.pitchManualPIDController.changePIDs(*self.pitchManualPIDControllerValues)
            self.rollManualPIDController.changePIDs(*self.rollManualPIDControllerValues)
            self.depthManualPIDController.changePIDs(*self.depthManualPIDControllerValues)
            self.xManualPIDController.changePIDs(*self.xManualPIDControllerValues)
            self.zManualPIDController.changePIDs(*self.zManualPIDControllerValues)
        else:
            self.yawAutonomousPIDControllerForwardModeValues = values[0]
            self.yawAutonomousPIDControllerBackwardsModeValues = values[1]
            self.pitchAutonomousPIDControllerValues = values[2]
            self.rollAutonomousPIDControllerValues = values[3]
            self.depthAutonomousPIDControllerValues = values[4]
            self.xAutonomousPIDControllerValues = values[5]
            self.zAutonomousPIDControllerValues = values[6]
            
            self.yawAutonomousPIDControllerForwardMode.changePIDs(*self.yawAutonomousPIDControllerForwardModeValues)
            self.yawAutonomousPIDControllerBackwardsMode.changePIDs(*self.yawAutonomousPIDControllerBackwardsModeValues)
            self.pitchAutonomousPIDController.changePIDs(*self.pitchAutonomousPIDControllerValues)
            self.rollAutonomousPIDController.changePIDs(*self.rollAutonomousPIDControllerValues)
            self.depthAutonomousPIDController.changePIDs(*self.depthAutonomousPIDControllerValues)
            self.xAutonomousPIDController.changePIDs(*self.xAutonomousPIDControllerValues)
            self.zAutonomousPIDController.changePIDs(*self.zAutonomousPIDControllerValues)
            
        
    def stopThread(self):
        self.running = False
        if self.manualMode == True:
            self.joystickController.killThread()
        self.sendDebugMessage("Stopping...")
        for i,v in enumerate(self.missionList):
            print "Test"
            v.executed = False
            v.readyToExecute = False
            v.reachedSpecificWaypoint = False
            v.locatedObstacles = False
            v.reachedGeneralWaypoint = False
            v.parameters["startTime"] = 0
        if self.MovementController != None:
            for i in range(0,9):
                self.maestroSerial.write(bytearray([0xFF, i, 0x7F]))
            self.MovementController = None
    
    def killThrusters(self):
        for i in range(0,9):
            self.maestroSerial.write(bytearray([0xFF, i, 0x7F]))

    #Main thread that is launched during autonomous run 
    def run(self):
        self.sendDebugMessage("Starting...")
        missionIndex = 0
        sentFlagMessage = False
        self.running = True
        waypointError = None
        
        
        '''
        This block of code is only called when in manual control mode, and there for does not use the mission code
        '''
        if self.manualMode == True and self.debug == False:
            controllerData = None
            self.pressedDepthChange = False
            self.desiredMoveDepth = 0
            controllerDepthButtonReleaseTimer = utilities.Timer()
            self.toggleLeftBumper = False
            self.toggleRightBumper = False
            self.quickButtonPressDepth = True
            while self.running:
                
                while len(self.joystickController.getList) > 0:
					controllerData = self.joystickController.getList.pop(0)
                
					print controllerData
                
					xPwm = 0
					zPwm = 0
					
					yDesiredRotation = 0
					xDesiredRotation = 0
					
					poseData = copy.copy(self.externalCommThread.orientation)
					poseData.append(self.externalCommThread.dvlData[3])
              
					if controllerData == None:
						print "No Controller Data"
						#continue
					else:                
						#print controllerData
						joystickInput = controllerData[1]
						buttonInput = controllerData[2]
						buttons = buttonInput
						hats = controllerData[3]
						
						if buttonInput[4] == 1 and self.pressedDepthChange == False:
							self.manualDepthValue -= 1
							self.pressedDepthChange = True
						if buttonInput[5] == 1 and self.pressedDepthChange == False:
							self.manualDepthValue += 1
							self.pressedDepthChange = True
						if buttonInput[4] == 0 and buttonInput[5] == 0:
							self.pressedDepthChange = False
						
						if buttonInput[7] == 1:
							for i in range(0,9):
								self.maestroSerial.write(bytearray([0xFF, i, 0x7F]))
						
						maxSpeed = 80
						
						xPwm = maxSpeed * joystickInput[0] * 2
						zPwm = maxSpeed * joystickInput[1] * -2
						
						poseData = copy.copy(self.externalCommThread.orientation)
						poseData.append(self.externalCommThread.dvlData[3])
						
						
						yDesiredRotation = maxSpeed/4 *  -joystickInput[4]
						xDesiredRotation = maxSpeed/4 *  -joystickInput[3]
						
						axis0, axis1, axis2, axis3, axis4 = int(joystickInput[0]*204), int(joystickInput[1]*204), int(joystickInput[2]*204), int(joystickInput[3]*204), int(joystickInput[4]*204)
							
				
						#DEPTH
						if hats[0][1] != 0: #Have the ability to increment depth
							if self.quickButtonPressDepth == True: #Eliminates Schmitt trigger effect
								self.desiredMoveDepth += -hats[0][1]*0.5
								if self.desiredMoveDepth < -1:
									self.desiredMoveDepth = -1
								controllerDepthButtonReleaseTimer.restartTimer()
								self.quickButtonPressDepth = False
								#print self.desiredMoveDepth, "depth inc"
						elif hats[0][1] == 0:
							netControllerDepthButtonReleaseTimer = controllerDepthButtonReleaseTimer.netTimer(controllerDepthButtonReleaseTimer.cpuClockTimeInSeconds())
							if netControllerDepthButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
								self.quickButtonPressDepth = True
								controllerDepthButtonReleaseTimer.restartTimer()
			  
						#TOGGLE ORIENTATION LOCK
						if buttons[5] == True:
							if self.quickButtonPressOrientationLock == True: #Eliminates Schmitt trigger effect
								self.toggleRightBumper = not self.toggleRightBumper
								self.quickButtonPressOrientationLock = False
						elif buttons[5] == False:
							self.quickButtonPressOrientationLock = True
							
						if buttons[4] == True:
							if self.quickButtonPressPositionLock == True: #Eliminates Schmitt trigger effect
								self.toggleLeftBumper = not self.toggleLeftBumper
								self.quickButtonPressPositionLock = False
								self.lockedPosition = self.dvlGuiData[0]
								currentDepth = self.medianExternalDepth
						elif buttons[4] == False:
							self.quickButtonPressPositionLock = True
							
						#ORIENTATION LOCK
						if self.toggleRightBumper == True and self.toggleLeftBumper == False: #Orientation lock
							if self.toggleLeftBumper == True:
								pass
								#print "Position and Orientation Lock"
								#poseData = [ahrsData[0], ahrsData[1], ahrsData[2], self.dvlGuiData[0][1], self.medianExternalDepth, self.dvlGuiData[0][0]]
								#self.thrusterPWMs, error, yawDesired = self.moveController.advancedMove(poseData, self.lockedPosition[1], self.desiredMoveDepth, self.lockedPosition[0], self.desiredMovePitch, self.desiredMoveYaw, self.desiredMoveRoll, 0)
								#self.desiredMissionOrientation = [True, self.desiredMoveYaw, ahrsData[0], ahrsData[1], ahrsData[2], self.lockedPosition[0], self.lockedPosition[1], self.desiredMoveDepth]
							else:
								print "Orientation Lock"
								self.thrusterPWMs = self.MovementController.advancedMove(poseData, axis0, self.desiredMoveDepth, -axis1, self.desiredMovePitch, self.desiredMoveYaw, self.desiredMoveRoll) #By not updating the ahrs value, it allows the last values from the ahrs before the button was pushed to be my new baseline
							
							if hats[0][0] != 0: #Have the ability to increment yaw while orientation is locked
								if self.quickButtonPressYaw == True: #Eliminates Schmitt trigger effect
									self.desiredMoveYaw = ((self.desiredMoveYaw + hats[0][0]*5))%360
									controllerYawButtonReleaseTimer.restartTimer()
									self.quickButtonPressYaw = False
									#print self.desiredMoveYaw, "yaw inc"
							elif hats[0][0] == 0:
								netControllerYawButtonReleaseTimer = controllerYawButtonReleaseTimer.netTimer(controllerYawButtonReleaseTimer.cpuClockTimeInSeconds())
								if netControllerYawButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
									self.quickButtonPressYaw = True
									controllerYawButtonReleaseTimer.restartTimer()
									
							if buttons[0] or buttons[3] != 0: #Have the ability to increment pitch while orientation is locked
								if self.quickButtonPressPitch == True: #Eliminates Schmitt trigger effect
									self.desiredMovePitch = self.desiredMovePitch + buttons[3] + (-1*buttons[0])
									controllerPitchButtonReleaseTimer.restartTimer()
									self.quickButtonPressPitch = False
									#print self.desiredMoveYaw, "yaw inc"
							elif buttons[0] == 0 and buttons[3] == 0:
								netControllerPitchButtonReleaseTimer = controllerPitchButtonReleaseTimer.netTimer(controllerPitchButtonReleaseTimer.cpuClockTimeInSeconds()) 
								if netControllerPitchButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
									self.quickButtonPressPitch = True
									controllerPitchButtonReleaseTimer.restartTimer()
									
							if buttons[2] or buttons[1] != 0: #Have the ability to increment roll while orientation is locked
								if self.quickButtonPressRoll == True: #Eliminates Schmitt trigger effect
									self.desiredMoveRoll = self.desiredMoveRoll + buttons[2] + (-1*buttons[1])
									controllerRollButtonReleaseTimer.restartTimer()
									self.quickButtonPressRoll = False
									#print self.desiredMoveYaw, "yaw inc"
							elif buttons[2] == 0 and buttons[1] == 0:
								netControllerRollButtonReleaseTimer = controllerRollButtonReleaseTimer.netTimer(controllerRollButtonReleaseTimer.cpuClockTimeInSeconds()) 
								if netControllerRollButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
									self.quickButtonPressRoll = True
									controllerRollButtonReleaseTimer.restartTimer()
									
						#Position Lock
						elif self.toggleLeftBumper == True and self.toggleRightBumper == False: # Position Lock
							#print self.lockedPosition
							poseData = [ahrsData[0], ahrsData[1], ahrsData[2], self.dvlGuiData[0][1], self.medianExternalDepth, self.dvlGuiData[0][0]]
							print "Position Lock"
							if self.subInPosition == False:
								self.thrusterPWMs, error, yawDesired = self.lockedMoveController.advancedMove(poseData, self.lockedPosition[1], self.desiredMoveDepth, self.lockedPosition[0], self.desiredMovePitch, self.desiredMoveYaw, self.desiredMoveRoll, 0, [False, axis4, axis3, -axis2])
							else:
								self.thrusterPWMs, error, yawDesired = self.lockedMoveController.advancedMove(poseData, self.lockedPosition[1], self.desiredMoveDepth, self.lockedPosition[0], self.desiredMovePitch, self.desiredMoveYaw, self.desiredMoveRoll, 0, [True, axis4, axis3, -axis2])
								
							xError, yError, zError = error[0], error[1], error[2]
							pitchError, yawError, rollError = error[3], error[4], error[5]
							
							if abs(xError) < 1 and abs(yError) < 1 and abs(zError) < 1:
								self.subInPosition = True
							else:
								self.subInPosition = False
									
						#Orientation and Position Lock
						elif self.toggleRightBumper == True and self.toggleLeftBumper == True:
							#print "Combo!!!!!"
							poseData = [ahrsData[0], ahrsData[1], ahrsData[2], self.dvlGuiData[0][1], self.medianExternalDepth, self.dvlGuiData[0][0]]
							self.thrusterPWMs, error, yawDesired = self.MovementController.advancedMove(poseData, self.lockedPosition[1], self.desiredMoveDepth, self.lockedPosition[0], self.desiredMovePitch, self.desiredMoveYaw, self.desiredMoveRoll, 0)
							
							if hats[0][0] != 0: #Have the ability to increment yaw while orientation is locked
								if self.quickButtonPressYaw == True: #Eliminates Schmitt trigger effect
									self.desiredMoveYaw = ((self.desiredMoveYaw + hats[0][0]*5))%360
									controllerYawButtonReleaseTimer.restartTimer()
									self.quickButtonPressYaw = False
									#print self.desiredMoveYaw, "yaw inc"
							elif hats[0][0] == 0:
								netControllerYawButtonReleaseTimer = controllerYawButtonReleaseTimer.netTimer(controllerYawButtonReleaseTimer.cpuClockTimeInSeconds())
								if netControllerYawButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
									self.quickButtonPressYaw = True
									controllerYawButtonReleaseTimer.restartTimer()
							
							if buttons[0] or buttons[3] != 0: #Have the ability to increment pitch while orientation is locked
								if self.quickButtonPressPitch == True: #Eliminates Schmitt trigger effect
									self.desiredMovePitch = self.desiredMovePitch + buttons[3] + (-1*buttons[0])
									controllerPitchButtonReleaseTimer.restartTimer()
									self.quickButtonPressPitch = False
									#print self.desiredMoveYaw, "yaw inc"
							elif buttons[0] == 0 and buttons[3] == 0:
								netControllerPitchButtonReleaseTimer = controllerPitchButtonReleaseTimer.netTimer(controllerPitchButtonReleaseTimer.cpuClockTimeInSeconds()) 
								if netControllerPitchButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
									self.quickButtonPressPitch = True
									controllerPitchButtonReleaseTimer.restartTimer()
									
							if buttons[2] or buttons[1] != 0: #Have the ability to increment roll while orientation is locked
								if self.quickButtonPressRoll == True: #Eliminates Schmitt trigger effect
									self.desiredMoveRoll = self.desiredMoveRoll + buttons[2] + (-1*buttons[1])
									controllerRollButtonReleaseTimer.restartTimer()
									self.quickButtonPressRoll = False
									#print self.desiredMoveYaw, "yaw inc"
							elif buttons[2] == 0 and buttons[1] == 0:
								netControllerRollButtonReleaseTimer = controllerRollButtonReleaseTimer.netTimer(controllerRollButtonReleaseTimer.cpuClockTimeInSeconds()) 
								if netControllerRollButtonReleaseTimer >= 0.01: #Need to have let go of it for at least 10 miliseconds to register as button not being pressed
									self.quickButtonPressRoll = True
									controllerRollButtonReleaseTimer.restartTimer()
									
							#self.desiredMissionOrientation = [True, self.desiredMoveYaw, ahrsData[0], ahrsData[1], ahrsData[2], self.lockedPosition[0], self.lockedPosition[1], self.desiredMoveDepth]
						#NORMAL OPERATION        
						elif self.toggleRightBumper == False and self.toggleLeftBumper == False:
							self.thrusterPWMs = self.MovementController.move(self.externalCommThread.position[2], axis0, self.desiredMoveDepth, -axis1, axis3, axis4, -axis2)
							self.desiredMoveYaw, self.desiredMovePitch, self.desiredMoveRoll = self.externalCommThread.orientation[0],self.externalCommThread.orientation[1],self.externalCommThread.orientation[2]
							self.desiredMissionOrientation = [False, 0, 0, 0, 0, 0, 0, 0]
							print "Under normal Operation, desired epth is: ", self.desiredMoveDepth
					
					#self.MovementController.move(poseData[3], xPwm, poseData[3], zPwm, xDesiredRotation, yDesiredRotation, 0)
					#self.MovementController.move(poseData[3], xPwm, self.manualDepthValue, zPwm, xDesiredRotation, yDesiredRotation, 0)
#                 try:
#                     self.MovementController.move(poseData[3], xPwm, poseData[3], zPwm, xDesiredRotation, yDesiredRotation, 0)
#                 except:
#                     print "Something Went Wrong:"
#                     print poseData[3], xPwm, poseData[3], zPwm, xDesiredRotation, yDesiredRotation, 0
                #self.MovementController.advancedMove(poseData, 3,0,0, poseData[1], poseData[0], poseData[2])
                
            print "Finished Manual Controll Loop"
            return
        
        '''
        This block of code is only called when NOT in manual control mode. It dictates the actuall movement of the sub when in autonomous mode
        '''
        while missionIndex < len(self.missionList) and self.running:
            
            currentOrientation = [0,0,0]
            currentLocation = [0,0,0]
            
            mission = self.missionList[missionIndex]
            if mission != self.currentMission:
                 self.sendDebugMessage("Starting Mission: " + mission.parameters["name"])
            self.currentMission = mission
            maxTime = int(mission.parameters["maxTime"])
            startTime = time.time()   
            
            #Modify the General Waypoint if it is set to use the same waypoint as another mission
            
            if mission.parameters["useGeneralWaypoint"] != None:
               print "Using Waypoint: ", mission.parameters["useGeneralWaypoint"]
               for i,v in enumerate(self.missionList):
                  if v.name == mission.parameters["useGeneralWaypoint"]:
                    mission.generalWaypoint = v.lastKnownPosition
                    break
            
            
            #while ((startTime - time.time()) <= maxTime or self.missionDebug==True) and self.running:
            while ((time.time()-startTime) <= maxTime) and self.running:
                #print mission.name
       		 	  
       		 	  
                if self.changeMission == True and missionIndex <= len(self.missionList)-1:
                    self.changeMission = None
                    missionIndex +=1
                    break
                elif self.changeMission == False and missionIndex >=0:
                    self.changeMission = None
                    missionIndex -= 1
                    break
                
                
                if mission.resetFlagBoolean == True:
                    sentFlagMessage = False
                    mission.resetFlagBoolean = False
                
                #Check for Socket Data from Computer Vision Process
                # NEED TO WRITE THIS CODE
                #socket.listen or something like that
                
                #This array will contain the position and orientation of the obstacle relative to the sub
                obstacleLocation = []
                #Collect Sensor Data
                
                if self.changeFlag != None:
                    sentFlagMessage = False
                    
                if self.changeFlag == True:
                    if mission.readyToExecute:
                        mission.executed = True
                    if mission.reachedSpecificWaypoint:
                        mission.readyToExecute = True
                    if mission.locatedObstacles:
                        mission.reachedSpecificWaypoint = True
                    if mission.reachedGeneralWaypoint:
                        mission.locatedObstacles = True
                    mission.reachedGeneralWaypoint = True
                elif self.changeFlag == False:
                    if mission.locatedObstacles == False:
                        mission.reachedGeneralWaypoint = False
                    if mission.reachedSpecificWaypoint == False:
                        mission.locatedObstacles = False
                    if mission.readyToExecute == False:
                        mission.reachedSpecificWaypoint = False
                    if mission.executed == False:
                        mission.readyToExecute = False
                    mission.readyToExecute= False
                    
                self.changeFlag = None               
                
                if not self.debug:
                    #This is where it will get position and orietnation data when the gui is not in debug mode
                    if mission.parameters["useKalmanFilter"] == True:
                        currentLocation = self.externalCommThread.position
                        currentOrientation = self.externalCommThread.orientation
                    else:
                        currentLocation = self.externalCommThread.position
                        currentOrientation = self.externalCommThread.orientation
                else:
                    self.missionDebug = True
                    
                
                
                #Check each flag to see if the mission is ready to move on 
                if not mission.reachedGeneralWaypoint:
                    #print "Haven't reached general waypoint"
                    reachedWaypoint = True
                    #Sends a message saying which flag it is on, but only once
                    if not sentFlagMessage:
                        self.sendDebugMessage("Begining General Waypoint")
                        print "Begining new waypoint"
                        sentFlagMessage = True
                        
                    if "ignoreGeneralWaypoint" in mission.parameters:
						#print "variable is set"
						if mission.parameters["ignoreGeneralWaypoint"] == "True":
							#print "Actually ignored it"
							self.reachedGeneralWaypoint = True
							continue
                    
                    if not self.debug:
                        if waypointError != None:
                            #print "Waypont Error: ", waypointError
                            #print "Genral Distance Error", mission.generalDistanceError
                            #print "Orientation error", mission.generalRotationError
                            if abs(waypointError[0]) < mission.generalDistanceError and abs(waypointError[1]) < mission.generalDistanceError and abs(waypointError[2]) < mission.generalDistanceError:
                                pass #This will only be called if we are actually at the waypoint in terms of position
                                #print "Not there position"
                            else:
                                reachedWaypoint = False
                                
                            if abs(waypointError[3]) < mission.generalRotationError and abs(waypointError[4]) <mission.generalRotationError and abs(waypointError[5]) < mission.generalRotationError:
                                pass #Only will be called if we have the correct orientaiton
                                #print "Not there orientation"
                            else:
                                reachedWaypoint = False
                        else:
                            print "Waypoint error was weird"
                            reachedWaypoint = False
                    
                    #print "Waypoint Status: ", reachedWaypoint
                    if reachedWaypoint and not self.missionDebug:
                    
                        print "Reahed the waypoint"
                        if mission.parameters["startTime"] == 0:
                            print "Reseting time"
                            mission.parameters["startTime"] = time.time()
                        
                        if time.time() - mission.parameters["startTime"] >= int(mission.parameters["waitTime"]):
                            mission.reachedGeneralWaypoint = True
                            mission.parameters["startTime"] = 0
                            print "Finished General Waypoint"
                            self.sendDebugMessage("Reached General Waypoint")
                            self.relativeMoveWaypoint = None
                            sentFlagMessage = False
                            '''
                            At this point we would tell the neural network to look for the object
                            socket.send("Look for: " + mission.obstacleName)
                            '''
                            continue
                        else:
                            print time.time() - mission.parameters["startTime"]						
                    #If we haven't reached the waypoint and the gui isn't in debug mode, then attempt to move to the general waypoint
                    if not self.debug:
						if mission.parameters["useRelativeWaypoint"] == "True":
							print "Using relative waypoint"
							if self.relativeMoveWaypoint == None:
								print "Going to: ", mission.generalWaypoint
								pose, n, e, u, x, y, z = self.MovementController.relativeMove(currentOrientation+currentLocation,None, None, None, None, None, None, mission.generalWaypoint[1], mission.generalWaypoint[2], mission.generalWaypoint[0], 
                                                              mission.generalWaypoint[4], mission.generalWaypoint[3], 0)
								self.relativeMoveWaypoint = [n, e, u, y, x, z]
                            #print "relative Waypoint: ",self.relativeMoveWaypoint    
							waypointError = self.MovementController.advancedMove(currentOrientation + currentLocation, self.relativeMoveWaypoint[0], self.relativeMoveWaypoint[1], mission.generalWaypoint[2], self.relativeMoveWaypoint[4], self.relativeMoveWaypoint[3], self.relativeMoveWaypoint[5])[1]		
						elif mission.parameters["useRelativeWorld"] == "True":
							print "Using relative world"
							if self.relativeMoveWaypoint == None:
								pose, n, e, u, x, y, z = self.MovementController.relativeMove(currentOrientation + currentLocation, mission.generalWaypoint[0], mission.generalWaypoint[1], mission.generalWaypoint[2], 
                                                              mission.generalWaypoint[4], mission.generalWaypoint[3], 0)
								self.relativeMoveWaypoint = [n,e,u,y,x,z]
							waypointError = self.MovementController.advancedMove(currentOrientation + currentLocation, self.relativeMoveWaypoint[0], self.relativeMoveWaypoint[1], mission.generalWaypoint[2], self.relativeMoveWaypoint[4], self.relativeMoveWaypoint[3], self.relativeMoveWaypoint[5])[1]		                               
						else:
							print "Using absolute"
							waypointError = self.MovementController.advancedMove(currentOrientation+currentLocation, mission.generalWaypoint[0], mission.generalWaypoint[1], mission.generalWaypoint[2], 
                                                              mission.generalWaypoint[4], mission.generalWaypoint[3], mission.generalWaypoint[5], mission.parameters["drivingMode"])[1]
						print "Waypoint Error: ", waypointError
                    continue
                
                
                
                #At this point it is suppose to turn until it locates the obstacle it is looking for
                #The obstacle data is coming in from the neural network process
                if not mission.locatedObstacles:
					if not sentFlagMessage:
						self.sendDebugMessage("Begining Object Detection")
						sentFlagMessage = True
					
					if not self.debug:
						foundObstacles = mission.lookForObstacles(self.externalCommThread, self.MovementController)
					if foundObstacles and not self.missionDebug:
						print "Found obstacles"
						mission.locatedObstacles = True
						sentFlagMessage = False  
					continue
                
                
                #Work with the neural network process and dynamically change the specificWaypoint to get
                #right in front of the obstacle or where ever we need to be
                if not mission.reachedSpecificWaypoint:
                    
                     #Sends a message saying which flag it is on, but only once
                    if not sentFlagMessage:
                        self.sendDebugMessage("Begining Specific Waypoint")
                        sentFlagMessage = True
                
                    reachedWaypoint = True
                    if not self.debug:
                        reachedWaypoint = mission.calculateSpecificWaypoint(self.externalCommThread, self.MovementController)
                    '''
                    if not self.debug:
                        for n,p in enumerate(currentLocation):
                            if not ((p + mission.specificDistanceError >= mission.specificWaypoint[n]) and (p - mission.specificDistanceError <= mission.specificWaypoint[n])):
                                reachedWaypoint = False
                        for n, p in enumerate(currentOrientation):
                            if not ((p - mission.specificRotationError <= mission.specificWaypoint[n+3]) and (p + mission.specificRotationError >= mission.specificWaypoint[n +3])):
                                reachedWaypoint = False
                    '''
                            
                    if reachedWaypoint and not self.missionDebug:
                        mission.reachedSpecificWaypoint = True
                        sentFlagMessage = False
                    continue
                
                #Do last minute alignment checks to make sure that we are ready to execute
                if not mission.readyToExecute:
                    
                     #Sends a message saying which flag it is on, but only once
                    if not sentFlagMessage:
                        self.sendDebugMessage("Begining Ready to Execute")
                        sentFlagMessage = True
                    
                    if not self.debug:
                        readyToExecute = mission.getExecutionPositionDifference(self.externalCommThread, self.MovementController)
                        if readyToExecute and not self.missionDebug:
							mission.readyToExecute = True
							sentFlagMessage = False
							continue
                    continue
                #Once ready to execute, EXECUTE!
                elif not mission.executed:
                    if not self.debug:
                        mission.executionTask(self.externalCommThread, self.MovementController)
                    self.sendDebugMessage("Executed!")
                    mission.executed = True
                    mission.success = True
                    missionIndex += 1
                    break
            
            if (time.time() - startTime) > maxTime:
				missionIndex += 1
                
        self.sendDebugMessage("Finished Run") 
        if self.debug == False:
            self.killThrusters()
