from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

try:
    from ADCDACPi import ADCDACPi
except ImportError:
    print("Failed to import ADCDACPi from python system path")
    print("Importing from parent folder instead")
    try:
        import sys
        sys.path.append('..')
        from ADCDACPi import ADCDACPi
    except ImportError:
        raise ImportError(
            "Failed to import library from parent folder")
import numpy as np
#from scipy import signal as sg


from time import sleep
import RPi.GPIO as GPIO
class Laser:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(21,GPIO.OUT)
        #GPIO.output(21,True)
        self.p = GPIO.PWM(21,500)
        self.p.start(0)

    def laser(self,pwr):
        self.p.ChangeDutyCycle(pwr)

    def laser_end(self):
        self.laser(0)
        GPIO.cleanup()

class Dac:
    def __init__(self):
        self.dac = ADCDACPi(1)

    def dacwrite(self,xyv):
        x,y = xyv
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > 2.047 or y > 2.047:
            print('volts nuts {} {}'.format(x,y))
            exit(1)
        self.dac.set_dac_voltage(1, x)  # set the voltage on channel 1 to 3.3V
        self.dac.set_dac_voltage(2, y)  # set the voltage on channel 1 to 3.3V



    
