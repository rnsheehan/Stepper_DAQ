"""
Python library for interfacing to Thorlabs KST101 Stepper Motor Controller

R. Sheehan 24 - 9 - 2026
"""

# Official Thorlab Examples on how to interface to their motion controllers can be found here: https://github.com/Thorlabs/Motion_Control_Examples
# Official Documentation on the various motion controller types can be found at the Thorlabs website
# Thorlabs KST101 Stepper Motor Controller: https://www.thorlabs.com/item/kst101?aID=e61f0f9fec8f33e359537d5f6dcb1c44&aC=1&aE=1&aN=1
# Thorlabs KDC101 Servo Motor Controller: https://www.thorlabs.com/item/KDC101?aID=6309be98e11ba9c1ec351552ac803536&aC=1
# Before proceeding with calling these examples you will need to have installed the appropriate hardware drivers on your PC
# Kinesis Software: https://www.thorlabs.com/software-pages/motion_control

import os
import time
import sys
import clr # package name is actually pythonnet: py -m pip install pythonnet

# Add References to .NET libraries
# Before proceeding with calling these examples you will need to have installed the appropriate hardware drivers on your PC
# Kinesis Software: https://www.thorlabs.com/software-pages/motion_control
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\\Program Files\\Thorlabs\\Kinesis\\ThorLabs.MotionControl.KCube.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.KCube.StepperMotorCLI import *
from System import Decimal  # necessary for real world units

class Stepper_Iface(object):

    # constructor
    def __init__(self, ser_num = None):
        """
        Constructor for the KST101 Stepper Motor

        ser_num (type: numeric string) is the serial number of the stepper motor controller that you wish to communicate with
        """
        try:
            # Error statement for exception handling
            self.MOD_NAME_STR = "KST101_Lib"
            self.FUNC_NAME = ".Stepper_Iface()" # use this in exception handling messages
            self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

            # Travel Limits in units of mm
            self.XLO = 0.0 # position lower bound
            self.XHI = 25.0 # position upper bound
            self.DX_MIN = (50.0/1.0e+6) # step-size minimum being set to 50 nm
            self.DX_MAX = 25 # step-size maximum being set to 50 nm
            
            # Stepper Motor Serial Number
            if ser_num.isnumeric():
                self.serial_no = ser_num
            else:
                self.serial_no = None
                self.ERR_STATEMENT = self.ERR_STATEMENT + '\nStepper Motor Serial Number is not in Correct Format'
                raise Exception

            self.Comms = False # Temporary, until I can get more info on the code

            # Open Comms
            self.OpenComms(True)

        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)

    # destructor
    # destructor  
    # https://www.geeksforgeeks.org/destructors-in-python/          
    def __del__(self):
        """
        close the link to the instrument object when it goes out of scope
        """
        
        if self.CommsStatus():
            # close the link to the device object when it goes out of scope
            
            #print('Closing Serial link with:',self.instr_obj.name)

            self.GoHome() # return the stepper to Home position before closing down

            # Stop Polling and Disconnect
            self.dev_obj.StopPolling()
            self.dev_obj.Disconnect()
        else:
            # Do nothing, no link to IBM4 established
            pass
            
    def __str__(self):
        """
        return a string the describes the class
        """
        
        return "class for interfacing to an KST101"

    def CommsStatus(self, loud = False):
        """
        investigate the status of the comms link
        """
        
        if self.Comms:
            if loud: print('Communication with: KST101-',self.serial_no,' is open')
            return True
        else:
            if loud: print('Communication with: KST101 is not open')
            return False

    def OpenComms(self, loud = False):
        """
        open comms with the stepper identified by the appropriate S/N
        """
        
        self.FUNC_NAME = ".OpenComms()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

        try:
            if self.serial_no is not None:
                # Initialise comms
                DeviceManagerCLI.BuildDeviceList()

                # instantiate a device object
                self.dev_obj = KCubeStepper.CreateKCubeStepper(self.serial_no)

                # Connect
                self.dev_obj.Connect(self.serial_no)
                time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

                # Get Device Information and display description
                self.device_info = self.dev_obj.GetDeviceInfo()
                if loud: print(self.device_info.Description)

                # Start polling and enable
                self.dev_obj.StartPolling(250)  #250ms polling rate
                time.sleep(0.25)

                self.dev_obj.EnableDevice()
                time.sleep(0.25)  # Wait for device to enable

                # Configure device
                self.use_file_settings = DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
                self.device_config = self.dev_obj.LoadMotorConfiguration(self.dev_obj.DeviceID, self.use_file_settings)

                self.Comms = True # Temporary, until I can get more info on the code
            else:
                self.ERR_STATEMENT = self.ERR_STATEMENT + '\nStepper Motor Serial Number is not defined\nCannot open comms'
                raise Exception
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)

    def GoHome(self):
        """
        Return the Stepper Motor To Home Position
        """

        self.FUNC_NAME = ".GoHome()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

        try:
            if self.CommsStatus():
                print("Homing Motor...")
                self.dev_obj.Home(60000)  # 60 seconds
                print("Motor Homed.")
            else:
                self.ERR_STATEMENT = self.ERR_STATEMENT + '\nComms with Stepper Motor is not established'
                raise Exception
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)

    def GoEmoh(self, loud = False):
        """
        Move the Stepper Motor To End Position
        """

        self.FUNC_NAME = ".GoEmoh()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

        try:
            self.SetLocation(self.XHI, loud)
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)

    def GetLocation(self, loud = False):
        """
        Report the current position of the stepper motor
        """

        # Need to be aware that self.dev_obj returns Position as a Decimal object
        # This can complicate the handling of the output
        # Some pages
        # https://docs.python.org/3/library/decimal.html
        # https://realpython.com/ref/stdlib/decimal/

        self.FUNC_NAME = ".GetLocation()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

        try:
            if self.CommsStatus():
                if loud: print(f'Current Position: {self.dev_obj.Position}') # this executes
                #print(type(self.dev_obj.Position))
                #if loud: print( 'Current Position: %(v1)0.6f (mm)'%{"v1":float(self.dev_obj.Position) } ) # this returns an error
                return self.dev_obj.Position
            else:
                self.ERR_STATEMENT = self.ERR_STATEMENT + '\nComms with Stepper Motor is not established'
                raise Exception
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)

    def SetLocation(self, new_position = 0.0, loud = False):
        """
        Set a new position for the stepper motor
        """

        self.FUNC_NAME = ".SetLocation()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

        try:
            c1 = self.CommsStatus()
            c2 = False if new_position < self.XLO else True
            c3 = False if new_position > self.XHI else True
            c10 = c1 and c2 and c3

            if c10:
                self.dev_obj.MoveTo(Decimal(new_position), 60000)
                time.sleep(1)
                if loud: self.GetLocation(loud)
            else:
                if not c1: self.ERR_STATEMENT = self.ERR_STATEMENT + '\nComms with Stepper Motor is not established'
                if not c2 or not c3: self.ERR_STATEMENT = self.ERR_STATEMENT + '\nnew_position is outside allowed range of motion'
                raise Exception
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)

    def TravelFixedSteps(self, n_stps = 1, strt_pos = 0.0, stp_size = 1.0, load = False):
        """
        Iterate movement over a finite sequence of steps

        n_stps (type: int) no. steps that stage must take
        strt_pos (type: float) starting travel position in units of mm
        stp_size (type: float) step size in units of mm for each step of the stepper
        """

        self.FUNC_NAME = ".TravelInSteps()" # use this in exception handling messages
        self.ERR_STATEMENT = "Error: " + self.MOD_NAME_STR + self.FUNC_NAME

        try:
            c1 = self.CommsStatus()
            c2 = False if strt_pos < self.XLO else True
            c3 = False if strt_pos > self.XHI else True
            c4 = True if n_stps > 1 else False
            c5 = True if stp_size >= self.DX_MIN and stp_size < self.DX_MAX else False
            c6 = True if strt_pos + n_stps * stp_size <= self.DX_MAX else False

            c10 = c1 and c2 and c3 and c4 and c5

            if c10:
                self.SetLocation(strt_pos, True)
                count = 0
                x0 = strt_pos
                while count < n_stps:
                    x0 = x0 + stp_size
                    self.SetLocation(x0, True)
                    count += 1
            else:
                if not c1: self.ERR_STATEMENT = self.ERR_STATEMENT + '\nComms with Stepper Motor is not established'
                if not c2 or not c3: self.ERR_STATEMENT = self.ERR_STATEMENT + '\nnew_position is outside allowed range of motion'
                raise Exception
        except Exception as e:
            print(self.ERR_STATEMENT)
            print(e)