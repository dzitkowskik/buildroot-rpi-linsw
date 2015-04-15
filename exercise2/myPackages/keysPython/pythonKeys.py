#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import os, sys
import os.path
import json

class GpioExporter(object):
    def __init__(self, number):
        self.number = number
        self.file = '/sys/class/gpio/gpio'+str(self.number)
        self.valueFile = self.file+'/value'
        self.directionFile = self.file+'/direction'

    def export(self):
        # self.unexport()
        with open('/sys/class/gpio/export', 'w') as f:
            f.write(str(self.number))

    def unexport(self):
        try:
            f = open('/sys/class/gpio/unexport', 'w')
            f.write(str(self.number))
            f.close()
        except IOError as e:
            print "Cannot unexport gpio "+str(self.number)+e.strerror+"\n"

class GPIO(GpioExporter):
    def __init__(self, number):
        super(GPIO, self).__init__(number)
        print "Create GPIO "+str(self.number)+"\n"
        self.export()

    def setValue(self, value):
        with open(self.valueFile, 'w') as f:
            f.write(str(value))

    def setDirection(self, dir):
        with open(self.directionFile, 'w') as f:
            f.write(str(dir))

    def getValue(self):
        with open(self.valueFile, 'r') as f:
            return int(f.read())

    def __del__(self):
        print "Delete GPIO "+str(self.number)+"\n"
        self.unexport()

class Led(GPIO):
    def __init__(self, number):
        super(Led, self).__init__(number)
        self.setDirection('out')

    def on(self):
        self.setValue(1)

    def off(self):
        self.setValue(0)

    def toggle(self):
        if self.getValue() == 0:
            self.on()
        else:
            self.off()

class Button(GPIO):
    state = 1

    def __init__(self, number):
        super(Button, self).__init__(number)
        self.setDirection('in')

    def pressed(self):
        result = False
        value = self.getValue()
        if value != self.state and value == 0:
            result = True
        self.state = value
        return result

# LEDS
led_red = Led(24)
led_green = Led(23)
led_white = Led(18)
led_blue = Led(17)

# BUTTONS
button_1 = Button(10)
button_2 = Button(27)
button_3 = Button(22)

def switchLedsOFF():
    led_red.off()
    led_green.off()
    led_white.off()
    led_blue.off()

def switchLedsON():
    led_blue.on()
    led_white.on()
    led_green.on()
    led_red.on()

def main():
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')

    switchLedsOFF()
    old_key = {}
    key = {}
    len = 4
    fileKey = '/tmp/klucz.key'
    if os.path.exists(fileKey):
        with open(fileKey, 'r') as f:
            old_key = {int(k):int(v) for k, v in json.load(f).items()}
        print "Podaj klucz naciskając przyciski aby odczytać wiadomość"

        while (len != 0):
            if button_1.pressed() is True:
                len -= 1
                key[len] = 1
            elif button_2.pressed() is True:
                len -= 1
                key[len] = 2
            elif button_3.pressed() is True:
                len -= 1
                key[len] = 3
            time.sleep(0.1)

        same = True
        for i in range(0, 4):
            if old_key[i] != key[i]:
                same = False

        if same is True:
            switchLedsON()
            os.remove(fileKey)
            print "Wiadomość: udało Ci się zapamiętać kod - jestś geniuszem!"
            time.sleep(3)
        else:
            print "Błędny kod - głupku!\n"
    else:
        print "Stwórz klucz naciskając przyciski..."
        print "Klucz musi być odpowiednio długi więc"
        print "Wpisuj kod aż nie zapali się czerwona dioda..."
        while (len != 0):
            if button_1.pressed() is True:
                len -= 1
                key[len] = 1
            elif button_2.pressed() is True:
                len -= 1
                key[len] = 2
            elif button_3.pressed() is True:
                len -= 1
                key[len] = 3

            if len == 3: led_blue.on()
            if len == 2: led_white.on()
            if len == 1: led_green.on()
            if len == 0: led_red.on()

            time.sleep(0.1)
        with open(fileKey, 'w') as f:
            json.dump(key, f)
        print "Zapisano klucz!"
        time.sleep(1)

    switchLedsOFF()

main()
