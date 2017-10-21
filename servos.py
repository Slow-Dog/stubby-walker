import time
import unittest
import pigpio

class Servos:

    #servo pin numbers
    _servos = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    _pigs = pigpio.pi() # Initialise pigpio functions, used for controlling servos

    #neutral offset. Pulswidth to add to get joint to zero
    #vagaries of construction mean that each joint's (really, the servo's) zero position isn't exact. This offset is added to the calculted angle to position each properly.
    #found by programmatically setting the robot leg positions to 90 degress and measuring
    _neutral = [0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0]

    #legServoPins = [[12, 8, 9], [5, 4, 17], [7, 14, 3], [18, 16, 19], [15, 13, 6], [2, 10, 11]]

    _servoAngleToPulsewidth = []


    def __init__(self):
        for servoNum in range(max(self._servos)+1):
            angleToPulsewidth = []
            for a in range(360):
                angle = a
                if a > 270:
                    angle = angle - 360
                pw = int((angle - 90) * 1000 / 90 + 1500)+self._neutral[servoNum]
                if (pw >= 500 and pw <= 2500):
                    angleToPulsewidth.append(pw)
                else:
                    angleToPulsewidth.append(0)
            self._servoAngleToPulsewidth.append(angleToPulsewidth)

    ##Set a servo to a position in degrees
    def setServoDegrees(self, servoNum, position ):
        ##Calls pigpio to set a servo to a position. 0 degrees is centered, so range is usually -90 to +90
        #print ("Servo {} {} degrees".format(servoNum, position))
        self._setServoPulsewidth(servoNum, self._servoAngleToPulsewidth[servoNum][position%360])

    def setAllServoDegrees(self, position):
        # switch all servos to given position
        for s in self._servos:
            self.setServoDegrees(s, position)

    def _setAllServoPulsewidth(self, pw):
        # switch all servos to centre position
        for s in self._servos:
            self._setServoPulsewidth(s, pw)

    def _setServoPulsewidth(self, servoNum, pw ):
        #print "Servo ", servoNum, " set to ", pw
        if (pw >= 500 and pw <= 2500):
            self._pigs.set_servo_pulsewidth(servoNum, pw)

    def centreDegrees(self):
        # switch all servos to leg centre position
        for s in self._servos:
            self.setServoDegrees(s, 0)

    def _centrePulse(self):
        # switch all servos to centre position
        for s in self._servos:
            self._setServoPulsewidth(s, 1500)

    def stop(self):
        # switch all servos off
        for s in self._servos:
            self._pigs.set_servo_pulsewidth(s, 0)

    def end(self):
        self.stop()
        self._pigs.stop()

##for s in servos:
##     pigs.set_servo_pulsewidth(s, 1500);

class TestServos(unittest.TestCase):

    def setUp(self):
        self.s = Servos()       
##       
##    def test_wave(self):
##        self.s.centre()
##        time.sleep(1)
##        for p in [1000, 2000, 1500]:
##            for l in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
###            self.s.setServo(l, 1000)
###            time.sleep(1)
###            self.s.setServo(l, 2000)
###            time.sleep(1)
##                self.s.setServo(l, p)
###            time.sleep(1)
##        time.sleep(1)
##        self.s.end()
##
    def test_Centre(self):
        self.s._centrePulse()
        time.sleep(1)
##        for a in range(60, 120):       
##            self.s.setAllServoDegrees(120-a)
        self.s.end()

##    def test_servoAngleToPulsewidth(self):
##        for snum in self.s._servos:
##            for a in [0,45,90,135,180]:
##                    print snum, a, self.s._servoAngleToPulsewidth[snum][a]
##            print

if __name__ == '__main__':
    unittest.main()
