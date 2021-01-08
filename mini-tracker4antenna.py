# /***************************************************
# Copyleft (c) 2021 Carlos Orts
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version. 
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses 
# ****************************************************/

# Import libraries
import RPi.GPIO as GPIO
import time
import sys
from decimal import *

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Read arguments
if len(sys.argv) == 1:
    print "Usage: "
    print " python mini-tracker4antenna.py [total pass time in minutes] [Start azimuth degrees] [End azimuth degrees] [Maximum elevation degrees]"
    print " python mini-tracker4antenna.py test"
    print " python mini-tracker4antenna.py ?"
    print "e.g: mini-tracker4antenna.py 9 37 140 60 "
    sys.exit()
elif sys.argv[1] == "?":
    print "Educational satellite tracking antenna device based on Raspberry Pi and SG92R servos."
    print "Usage: "
    print " python mini-tracker4antenna.py [total pass time in minutes] [Start azimuth degrees] [End azimuth degrees] [Maximum elevation degrees]"
    print " python mini-tracker4antenna.py test"
    print " python mini-tracker4antenna.py ?"
    print "e.g: mini-tracker4antenna.py 9 37 140 60 "
    sys.exit()

if sys.argv[1] != "test":
    PassTime = int(sys.argv[1]) # in minutes
    StartAZ = int(sys.argv[2])  # in degrees
    EndAZ = int(sys.argv[3])    # in degrees
    MaxEL = int(sys.argv[4])    # in degrees

# Setup variables
FitAZ = 0  # Azimuth device adjustment
FitEL = 15 # Elevation device adjustment

print ("Servos initialization...")

# Set pins as an output, and set servos as PWM
GPIO.setup(11,GPIO.OUT)
ServoAzimuth = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse
GPIO.setup(13,GPIO.OUT)
ServoElevation = GPIO.PWM(13,50) # Note 13 is pin, 50 = 50Hz pulse

# start PWM running, but with value of 0 (pulse off)
ServoAzimuth.start(0)
time.sleep(1)
ServoElevation.start(0)
time.sleep(1)

# move the ServoAzimuth for Azimuth
def MoveAzimuth(angle):
    duty = ( angle + FitAZ) / 18 + 2
    print "  Azimuth: ",angle
    GPIO.output(11, True)
    ServoAzimuth.ChangeDutyCycle(duty)
    time.sleep(.5)
    GPIO.output(11, False)
    ServoAzimuth.ChangeDutyCycle(0)

# move the ServoElevation for elevation
def MoveElevation(angle):
    duty = ( angle + FitEL ) / 18 + 2
    print "  Elevation: ",angle
    GPIO.output(13, True)
    ServoElevation.ChangeDutyCycle(duty)
    time.sleep(.5)
    GPIO.output(13, False)
    ServoElevation.ChangeDutyCycle(0)

# test
def Test():
    MoveAzimuth(0)
    time.sleep(.3)
    MoveElevation(0)
    time.sleep(.3)
    MoveAzimuth(45)
    time.sleep(.3)
    MoveElevation(35)
    time.sleep(.3)
    MoveAzimuth(90)
    time.sleep(.3)
    MoveElevation(45)
    time.sleep(.3)
    MoveAzimuth(135)
    time.sleep(.3)
    MoveElevation(60)
    time.sleep(.3)
    MoveAzimuth(180)
    time.sleep(.3)
    MoveElevation(45)
    time.sleep(.3)
    MoveAzimuth(0)
    time.sleep(.3)
    MoveElevation(0)
    time.sleep(.3)

if sys.argv[1] == "test":
    Test()
else:
    Steps = PassTime * 2 # One motor step every 30 s
    AZStepAngle = Decimal( EndAZ - StartAZ ) / Decimal(Steps) # Azimuth Angle of one step
    # Elevation calculation based on a quadratic equation of a parabolic curve
    StepsMaxEL = Steps / 2
    OriginCoefficient = ( -1 * Decimal(MaxEL) / ( Decimal(StepsMaxEL) ** 2 )) # Coefficient of 0.0 origin

    # Begin of movement
    for i in range (Steps+1):
        angleAZ = StartAZ + ( i * AZStepAngle )
        angleEL = MaxEL + ( OriginCoefficient * (( i - StepsMaxEL ) ** 2))
        print "Pass complete:", int(round(Decimal(i*100/(Steps+1)))), "%"
        MoveAzimuth(int(round(angleAZ)))
        time.sleep(.5)
        MoveElevation(int(round(angleEL)))
        time.sleep(29)

    # 0.0 location
    MoveAzimuth(0)
    time.sleep(.3)
    MoveElevation(0)
    time.sleep(.3)

# Clean things up at the end
ServoAzimuth.stop()
ServoElevation.stop()
GPIO.cleanup()
print ("Goodbye")
