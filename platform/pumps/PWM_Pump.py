#!/usr/bin/env python

import gpio
import time

class Pump(object):

    def __init__(self, gpio_str):
        self.gpio_str = gpio_str
        self.setup()

    def setup(self):
        gpio.pinMode(self.gpio_str, gpio.OUTPUT)

    def on(self):
        gpio.digitalWrite(self.gpio_str, gpio.HIGH)

    def off(self):
        gpio.digitalWrite(self.gpio_str, gpio.LOW)

##    def pwm(self, value):
##        self.on()
##        time.sleep(value)
##        self.off()
##        #time.sleep(value)
##        gpio.digitalWrite(self.gpio_str, gpio.HIGH)
##        time.sleep(value/10)
##        gpio.digitalWrite(self.gpio_str, gpio.LOW)
##        time.sleep(value/10)
        
    def run(self, delay):
        self.on()
        time.sleep(delay)
        self.off()
        



##pump_pin = ["gpio2","gpio3","gpio4","gpio5","gpio6","gpio7","gpio8","gpio9"]
##def delay(ms):
##    time.sleep(1.0*ms/1000)
##
##def setup():
##    for i in range (8):
##	 print i
##	 gpio.pinMode(pump_pin[i], gpio.OUTPUT)
##	
##def loop():
##    while(1):
##	for j in range (8):
##		print pump_pin[j]
##        	gpio.digitalWrite(pump_pin[j], gpio.HIGH)
##        	delay(200)
##        	gpio.digitalWrite(pump_pin[j], gpio.LOW)
##        	delay(100)
##
##def main():
##    setup()
##    loop()
