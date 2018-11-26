from motobit import MotoBit

import time
import random

class Robot:    
    def __init__(self, i2c):
        motobit = MotoBit(i2c)
        self._left_wheel = motobit.left_motor(invert=True)
        self._right_wheel = motobit.right_motor(invert=True)
        motobit.enable()
        self.moving = False
        self._left_wheel.forward(0)
        self._right_wheel.forward(0)

    def reverse(self, speed=30):
        self._left_wheel.reverse(speed)
        self._right_wheel.reverse(speed)

    def start(self, speed=40):
        self.moving = True
        for i in range(0, speed, 5):
            self._left_wheel.forward(i-4)
            self._right_wheel.forward(i)
            time.sleep(0.1)

    def stop(self):
        self._left_wheel.forward(0)
        self._right_wheel.forward(0)
        self.moving = False
        
    def turn_counter_clockwise(self, speed=30):
        self._left_wheel.reverse(speed)
        self._right_wheel.forward(speed)

    def turn_clockwise(self, speed=30):
        self._left_wheel.forward(speed)
        self._right_wheel.reverse(speed)
        
    def evade(self):        
        self.reverse()
        time.sleep(1.0)
        self.stop()
        random.choice([self.turn_clockwise, self.turn_counter_clockwise])()
        time.sleep(random.choice([0.5, 0.9, 1.2]))
        self.stop()