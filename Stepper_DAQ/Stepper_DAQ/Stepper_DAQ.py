# Import various modules

from ast import Try, TryStar
import os
from pickle import FALSE

import Basic_Examples

"""
The aim of this project is to establish a code for working with Thorlabs Stepper Motors, Translation and Rotation Stages of Various Kinds
It should also be possible for the code to interact with other instruments that may form part of an experimental setup, such as the NI-DAQ

Official Thorlab Examples on how to interface to their motion controllers can be found here: https://github.com/Thorlabs/Motion_Control_Examples

Project Dependencies
Implementation of the NI_DAQ_Lib Module can be found here: https://github.com/rnsheehan/NI_DAQ_6001
Implementation of the Common Module can be found here: https://github.com/rnsheehan/Common
Implementation of the Plotting Module can be found here: https://github.com/rnsheehan/Plotting
Implementation of the Sweep Interval Module can be found here: https://github.com/rnsheehan/SweepInt

R. Sheehan 23 - 9 - 2026
"""

MOD_NAME_STR = "Stepper_DAQ"

def main():
    pass

if __name__ == '__main__':
    main()

    pwd = os.getcwd() # get current working directory

    print(pwd)

    Basic_Examples.KST101_Loop()