"""
Module illustrating basic interfaces to various motion controllers

R. Sheehan 23 - 9 - 2026
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

MOD_NAME_STR = "Basic_Examples"

def KST101_Loop():
    """
    initialise comms with KST101, home the device, perform a loop over some steps, home the device again
    R. Sheehan 22 - 9 - 2026
    """

    FUNC_NAME = ".KST101_Loop()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # Initilise comms
        DeviceManagerCLI.BuildDeviceList()

        # create new device
        serial_no = "26003991"  # Replace this line with your device's serial number
        device = KCubeStepper.CreateKCubeStepper(serial_no)

        # Connect
        device.Connect(serial_no)
        time.sleep(0.25)  # wait statements are important to allow settings to be sent to the device

        # Get Device Information and display description
        device_info = device.GetDeviceInfo()
        print(device_info.Description)

        # Start polling and enable
        device.StartPolling(250)  #250ms polling rate
        time.sleep(0.25)
        device.EnableDevice()
        time.sleep(0.25)  # Wait for device to enable

        # Configure device
        use_file_settings = DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings
        device_config = device.LoadMotorConfiguration(device.DeviceID, use_file_settings)

        # Home device
        HOME_AT_START = False
        if HOME_AT_START:
            print("Homing Motor...")
            device.Home(60000)  # 60 seconds
            print("Motor Homed.")
            print(f'Position After Homing: {device.Position}')

        # Get/Set Velocity Params
        device_vel_params = device.GetVelocityParams()

        print("device_vel_params: ",device_vel_params)        
        print(f'Acceleration: {device_vel_params.Acceleration}',
              f'Velocity: {device_vel_params.MaxVelocity}')

        # Move to midpoint of travel range
        x0 = 5
        new_pos = Decimal(x0)  # in Real Units
        device.MoveTo(new_pos, 60000) # 60 seconds
        current_pos = device.Position
        print(current_pos)
        print(f'Current Position: {device.Position}')
        print()

        # loop over a sequence of movements
        n_moves = 100
        #delta_x = 5.0/1000.0 # 5um units of mm
        delta_x = 500.0/1.0E+6 # 100nm units of mm
        print("")
        print("Step-size: ",1000.0*delta_x," (um)")
        print("Total Displacement: ",1000.0*n_moves*delta_x," (um)")
        print("Freq-Space Separation: ",1.0/(1000.0*n_moves*delta_x),"(um)^{-1}")
        print("")
        count = 0
        while count < n_moves:
            x0 = x0 + delta_x # in Real Units
            #print(x0)
            #new_pos = Decimal(x0) # in Real Units
            device.MoveTo(Decimal(x0), 60000) # 60 seconds
            time.sleep(1)
            print(f'Current Position: {device.Position}')
            count = count + 1
        print(f'Current Position: {device.Position}')

        HOME_AT_END = True
        if HOME_AT_END:
            print("Homing Motor...")
            device.Home(60000)  # 60 seconds
            print("Motor Homed.")
            print(f'Position After Homing: {device.Position}')

        # Stop Polling and Disconnect
        device.StopPolling()
        device.Disconnect()

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)