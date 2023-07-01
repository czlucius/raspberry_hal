import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MATRIX = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          ['*', 0, '#']]  # layout of keys on keypad
ROW = [6, 20, 19, 13]  # row pins
COL = [12, 5, 16]  # column pins

class HALKeypad:
    def __init__(self, callbacks=None, run_in_background=True):
        self.callbacks: list = callbacks if callbacks else []
        self.should_listen: bool = True
        if run_in_background:
            self.thread = Thread(target=self.get_key)
            self.thread.start()

    def stop_listening(self):
        self.should_listen = False

    def start_listening(self):
        self.should_listen = True

    def add_callback(self, callback):
        self.callbacks.append(callback)
        # self.call


    def callback(self, *args, **kwargs):
        for cb in self.callbacks:
            cb(*args, **kwargs)

    def get_key(self):
        # scan keypad
        while (True):
            if self.should_listen:
                for i in range(3):  # loop thru’ all columns
                    GPIO.output(COL[i], 0)  # pull one column pin low
                    for j in range(4):  # check which row pin becomes low
                        if GPIO.input(ROW[j]) == 0:  # if a key is pressed
                            # print (MATRIX[j][i]) #print the key pressed
                            self.callback(MATRIX[j][i])
                            # return MATRIX[j][i]

                            while GPIO.input(ROW[j]) == 0:  # debounce
                                sleep(0.1)
                    GPIO.output(COL[i], 1)  # write back default value of 1

