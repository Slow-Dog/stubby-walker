import threading
import unittest

class breathe:

    def __init__(self, breatheHeight, breathDurationMilliseconds):
        self._breatheHeight = breatheHeight
        self._currentBreatheHeight = 0
        self._breatheTime = breathDurationMilliseconds
        self._breatheDirection = 1
        self._breatheRateUp = 1
        self._breatheRateDown = self._breatheRateUp*3
        self.setBreathTick()
        self._t = threading.Timer(self._breathTick, self.tick, ())

    def setBreathTick(self):
        if self._breatheDirection == 1:
            self._breathTick = self._breatheTime/self._breatheHeight*self._breatheRateUp/1000.0
        else:
            self._breathTick = self._breatheTime/self._breatheHeight*self._breatheRateDown/1000.0


    def tick(self):
        self._currentBreatheHeight = self._currentBreatheHeight + self._breatheDirection

        ##print self._currentBreatheHeight

        if self._currentBreatheHeight <= 0 or self._currentBreatheHeight >= self._breatheHeight:
            self._breatheDirection = - self._breatheDirection
            self.setBreathTick()
        if self._breatheDirection <> 0:
            threading.Timer(self._breathTick, self.tick, ()).start()

    def stop(self):
        self._breatheDirection = 0

    def start(self):
        self._breatheDirection = 1
        self.setBreathTick()
        threading.Timer(self._breathTick, self.tick, ()).start()
