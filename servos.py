import pigpio
import time
import unittest

class Servos:

  #servo pin numbers
  _servos = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
  _pigs = pigpio.pi() # Initialise pigpio functions, used for controlling servos

  def __init__(self):
    i=0

  ##Set a servo to a position in degrees
  def setServoDegrees (self, servoNum, position ):
    ##Calls pigpio to set a servo to a position. 0 degrees is centred, so range is usually -90 to +90
    #      print ("Servo {} {} micro pulses".format(s, pw))
    pw = int (round(position * 500.0 / 90.0 + 1500))
    if (pw>=500 and pw <=2500) :
      self._pigs.set_servo_pulsewidth(servoNum, pw)

  def setAllServoDegrees(self, position):
    # switch all servos to centre position
    for s in self._servos:
      self.setServoDegrees(s, position);

  def setServo (self, servoNum, pw ):
#    print "Servo ", servoNum, " set to ", pw 
    if (pw>=500 and pw <=2500) :
      self._pigs.set_servo_pulsewidth(servoNum, pw)

  def centre(self):
    # switch all servos to centre position
    for s in self._servos:
      self.setServoDegrees(s, 90);
    
    self.stop()

  def stop(self):
    # switch all servos off
    for s in self._servos:
      self._pigs.set_servo_pulsewidth(s, 0);

  def end(self):
    self.stop()
    self._pigs.stop()


##for s in servos:
##   pigs.set_servo_pulsewidth(s, 1500);

##class TestServos(unittest.TestCase):
## 
##  def setUp(self):
##    self.s=Servos()
##    self.s.end()
##    
##  def test_wave(self):
##    self.s.centre()
##    time.sleep(1)
##    for p in [1000, 2000, 1500]:
##      for l in [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]:
###      self.s.setServo(l,1000)
###      time.sleep(1)
###      self.s.setServo(l,2000)
###      time.sleep(1)
##        self.s.setServo(l,p)
###      time.sleep(1)
##    time.sleep(1)
##    self.s.end()
## 
####  def test_Centre(self):
####    self.s.centre()
####    time.sleep(1)
####    for a in range(60, 120):    
####      self.s.setAllServoDegrees(120-a)
####    time.sleep(1)
####    self.s.centre()
####    time.sleep(1)
####    self.s.end()
##
##if __name__ == '__main__':
##    unittest.main()

