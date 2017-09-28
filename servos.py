import pigpio

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

  def setServo (self, servoNum, pw ):
  ##  print "Servo ", servoNum, " set to ", pw 
    if (pw>=500 and pw <=2500) :
      self._pigs.set_servo_pulsewidth(servoNum, pw)

  def centre(self):
    # switch all servos to centre position
    for s in self._servos:
      self._pigs.set_servo_pulsewidth(s, 1500);
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
