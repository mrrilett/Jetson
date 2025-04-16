# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:09:39 2023

@author: micha
"""

#Add dependencies
import xarm 
import time
import random

arm = xarm.Controller('USB')
rockpaperscissors = random.randint(1,3)
#rockpaperscissors = 2

def initial_position(arm):
    arm.setPosition([[1,500],[2, 500],[3, 500],[4,500],[5,500],[6,500]])

def pick_and_place(arm):
    if (rockpaperscissors == 1):
        arm.setPosition(4,700)
        time.sleep(1)
        arm.setPosition(4,535)
        time.sleep(1)
        arm.setPosition(4,700)
        time.sleep(1)
        arm.setPosition(4,535)
        time.sleep(1)
        arm.setPosition([[1,695],[3, 110],[4, 815],[5,675]])
        time.sleep(3)
        print("ROCK")
        arm.setPosition([[1,500],[3, 500],[4, 500],[5,500]])
    elif (rockpaperscissors == 2):
        arm.setPosition(4,700)
        time.sleep(1)
        arm.setPosition(4,535)
        time.sleep(1)
        arm.setPosition(4,700)
        time.sleep(1)
        arm.setPosition(4,535)
        time.sleep(1)
        arm.setPosition([[1,695],[3, 360],[4, 580],[5,415]])
        time.sleep(3)
        print ("PAPER")
        arm.setPosition([[1,500],[3, 500],[4, 500],[5,500]])
    else:
        arm.setPosition(4,700)
        time.sleep(1)
        arm.setPosition(4,535)
        time.sleep(1)
        arm.setPosition(4,700)
        time.sleep(1)
        arm.setPosition(4,535)
        time.sleep(1)
        arm.setPosition([[1,260],[2, 140],[3, 360],[4,745],[5,610]])
        time.sleep(1)
        print ("SCISSORS")
        arm.setPosition(1,705)
        time.sleep(1)
        arm.setPosition([[1,260],[2, 140],[3, 360],[4,745],[5,610]])
        time.sleep(1)
        arm.setPosition(1,705)
        time.sleep(1)
        arm.setPosition([[1,260],[2, 140],[3, 360],[4,745],[5,610]])
        time.sleep(1)
        arm.setPosition(1,705)
        time.sleep(1)
        arm.setPosition([[1,500],[3, 500],[4, 500],[5,500]])
    


#serial_device.SetPosition([14], [1450])
# serial_device.SetPosition([5], [375])
# time.sleep(1)
# serial_device.SetPosition([1], [750])
# serial_device.SetPosition([4], [437])
# serial_device.SetPosition([1], [250])
# serial_device.SetPosition([4], [500])
# serial_device.SetPosition([5], [500])
# serial_device.SetPosition([6], [750])
# serial_device.SetPosition([5], [375])
# serial_device.SetPosition([4], [437])
# serial_device.SetPosition([1], [750])
# serial_device.SetPosition([5], [500])
# serial_device.SetPosition([4], [500])
# serial_device.SetPosition([1], [500])
# serial_device.SetPosition([6], [500])

initial_position(arm)
time.sleep(2)
pick_and_place(arm)
time.sleep(2)
initial_position(arm)

#Can add loop to ask user to go again or not
