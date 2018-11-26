import gc
print(gc.mem_free())
gc.collect()

from robot import Robot
from guidance import StuckEvasion
from guidance import ObstacleAvoidance

import adafruit_vl6180x
import adafruit_amg88xx

import busio
import board
import time
import math

import neopixel
from digitalio import DigitalInOut, Direction, Pull

class UI:
    def __init__(self):
        self.led = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.current = 0
        self.direction = 1
        self.last_time = time.monotonic()

    def call_for_help(self):
        while not button_pressed(button):
            self.flash(50, 0, 0)

    def flash(self, r=0, g=0, b=0):
        for i in range(3):
            self.led.fill((r, g, b))
            self.lights_distress((r, g, b))
            time.sleep(0.5)
            self.led.fill((0, 0, 0))
            self.lights_distress((0, 0, 0))
            time.sleep(0.2)
            
    def ok(self):
        self.led.fill((0, 50, 0))
        self.lights_on()
        time.sleep(0.5)

    def off(self):
        self.led.fill((0, 0, 0))
        self.lights_off()
        
    def lights_distress(self, rgb):
        global pixels
        pixels.fill(rgb)
    
        
    def lights_off(self):
        global pixels
        pixels.fill((0, 0, 0))

    def lights_on(self):
        global pixels
        pixels.fill((18, 0, 0))
        
    def kitt_effect(self):
        global pixels
 
        if time.monotonic() - self.last_time > 0.1:
            
            pixels[self.current] = (200, 0, 0)

            if self.direction == 1 and self.current > 0:
                pixels[self.current-1] = (18, 0, 0)
            elif self.direction == -1 and self.current < 7:
                pixels[self.current+1] = (18, 0, 0)

            self.current += self.direction
            
            if self.current > 7:
                self.current = 7
                self.direction = -1
            elif self.current < 0:
                self.current = 0
                self.direction = 1
                
            pixels.show()
                
            self.last_time = time.monotonic()
        
        
button = DigitalInOut(board.D12)
button.direction = Direction.INPUT
button.pull = Pull.DOWN

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl6180x.VL6180X(i2c)
#amg = adafruit_amg88xx.AMG88XX(i2c)
robot = Robot(i2c)
ui = UI()
print(gc.mem_free())
pixels = neopixel.NeoPixel(board.D13, 8)

pixels.fill((0,0,0))

# Define a gamma correction lookup table to make colors more accurate.
# See this guide for more background on gamma correction:
#   https://learn.adafruit.com/led-tricks-gamma-correction/
gamma8 = bytearray(256)
for i in range(len(gamma8)):
    gamma8[i] = int(math.pow(i/255.0, 2.8)*255.0+0.5) & 0xFF

# Define a function to convert from HSV (hue, saturation, value) color to
# RGB colors that DotStar LEDs speak.  The HSV color space is a nicer for
# animations because you can easily change the hue and value (brightness)
# vs. RGB colors.  Pass in a hue (in degrees from 0-360) and saturation and
# value that range from 0 to 1.0.  This will also use the gamma correction
# table above to get the most accurate color.  Adapted from C/C++ code here:
#   https://www.cs.rit.edu/~ncs/color/t_convert.html
def HSV_to_RGB(h, s, v):
    r = 0
    g = 0
    b = 0
    if s == 0.0:
        r = v
        g = v
        b = v
    else:
        h /= 60.0       # sector 0 to 5
        i = int(math.floor(h))
        f = h - i       # factorial part of h
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        if i == 0:
            r = v
            g = t
            b = p
        elif i == 1:
            r = q
            g = v
            b = p
        elif i == 2:
            r = p
            g = v
            b = t
        elif i == 3:
            r = p
            g = q
            b = v
        elif i == 4:
            r = t
            g = p
            b = v
        else:
            r = v
            g = p
            b = q
    r = gamma8[int(255.0*r)]
    g = gamma8[int(255.0*g)]
    b = gamma8[int(255.0*b)]
    return (r, g, b)

# Another handy function for linear interpolation of a value.  Pass in a value
# x that's within the range x0...x1 and a range y0...y1 to get an output value
# y that's proportionally within y0...y1 based on x within x0...x1.  Handy for
# transforming a value in one range to a value in another (like Arduino's map
# function).
def lerp(x, x0, x1, y0, y1):
    return y0+(x-x0)*((y1-y0)/(x1-x0))

def button_pressed(button):
        val = button.value
        time.sleep(0.05)
        return val and not button.value


while True:    
    if button_pressed(button):
        obstacle_avoidance = ObstacleAvoidance()
        stuck_evasion = StuckEvasion()
        ui.ok()
        robot.start()
    
    while robot.moving:
        ui.kitt_effect()
        
        obstacle_range = sensor.range
        obstacle_avoidance.perform(ui, robot, obstacle_range)
        stuck_evasion.perform(ui, robot, obstacle_range)
        
        if button_pressed(button):
            ui.off()
            robot.stop()
            time.sleep(1)

        time.sleep(0.04)