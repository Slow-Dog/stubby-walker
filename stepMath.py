import math
import mathLookup
import vectorMath
import unittest

#Handles gait functions

#Initialises current position at the zero position in the step cycle, which is where the position = step size)
#Step increments the current position, outputting a body position for each set of legs that makes that step:
# If you want to move the robot, the body position for the set of legs on the ground is incremented,
# while the body position for the legs in the air in decremented.
# i.e. The legs on the ground move backwards, and the legs in the air move forward.
#If the movement passes "stepLength", the legs swap over.


class StepMath:

  def __init__(self, stepLength, angleSize, stepHeight):
    self._stepLength=stepLength
    self._stepLength2=stepLength*2
    self._stepLength4=stepLength*4
    self._angleSize=angleSize
    self._angleSize2=angleSize*2
    self._angleSize4=angleSize*4
    self._xCyclePos=stepLength
    self._yCyclePos=stepLength
    self._angleCyclePos=angleSize
    self._stepHeight = stepHeight

    #phase 0 = leg 0 (Left) down , 1 Leg 0 up
    self._phase=0

  def whatPhaseLength (self, position): 
    return ((position)/(self._stepLength2))%2

  def whatPhaseAngle (self, position): 
    return ((position)/(self._angleSize2))%2

  def allRelativeBodyPositionsFromStep(self, xDistanceStepped, yDistanceStepped, angleStepped):
    bodyPosition=[[]]*6
    bodyRotation=[[]]*6
    leftPos, leftAngle, rightPos, rightAngle = self.relativeBodyPositionsFromStep( xDistanceStepped, yDistanceStepped, angleStepped)
    #left Leg
    for i in range(0, 6, 2):
      bodyPosition[i]=leftPos
      bodyRotation[i]=leftAngle
    #right Leg
    for i in range(1, 6, 2):
      bodyPosition[i]=rightPos
      bodyRotation[i]=rightAngle
    return bodyPosition, bodyRotation

  ##Moves body given x, y, and angle stepped through.
  ##Returns equivalent body positions and rotations to use for each tripod set of legs.
  def relativeBodyPositionsFromStep(self, xDistanceStepped, yDistanceStepped, angleStepped):
    leftStep, leftIsUp, rightStep, rightIsUp = self.step(xDistanceStepped, yDistanceStepped, angleStepped)

    leftPos = [leftStep[0], leftStep[1], leftIsUp*-self._stepHeight]
    leftAngle = [0, 0, leftStep[2]]
    rightPos = [rightStep[0], rightStep[1], rightIsUp*-self._stepHeight]
    rightAngle = [0, 0, rightStep[2]]

    return leftPos, leftAngle, rightPos, rightAngle

  ##Swaps which set of legs are raised.
  def relativeBodyPositionsFromTap(self):
    self._phase = 1-self._phase
    self._xCyclePos=self.stepFlip(self._xCyclePos)
    self._yCyclePos=self.stepFlip(self._yCyclePos)
    self._angleCyclePos=self.angleFlip(self._angleCyclePos)
    leftStep, leftIsUp, rightStep, rightIsUp = self.returnLeftAndRightFromPosition()

    leftPos = [leftStep[0], leftStep[1], leftIsUp*-self._stepHeight]
    leftAngle = [0, 0, leftStep[2]]
    rightPos = [rightStep[0], rightStep[1], rightIsUp*-self._stepHeight]
    rightAngle = [0, 0, rightStep[2]]

    return leftPos, leftAngle, rightPos, rightAngle

  ##Moves body given x,y,angle.
  ##Returns equivalent x, y, angle to use for each set of legs.
  def step(self, x, y, angle):

    ##First determine where in the 0-stepLength4 cycle the body is
    ##For x, the y, the angle.
    ##If any crosses a phase boundary,
    ##flip the other axes to the equivalent position in the cycle for the opposite phase
    self._xCyclePos=(self._xCyclePos+x)%self._stepLength4
    newPhase = self.whatPhaseLength(self._xCyclePos)
    if (newPhase <> self._phase):
      self._phase = newPhase
      self._yCyclePos=self.stepFlip(self._yCyclePos)
      self._angleCyclePos=self.angleFlip(self._angleCyclePos)

    self._yCyclePos=(self._yCyclePos+y)%self._stepLength4
    newPhase = self.whatPhaseLength(self._yCyclePos)
    if (newPhase <> self._phase):
      self._phase = newPhase
      self._xCyclePos=self.stepFlip(self._xCyclePos)
      self._angleCyclePos=self.angleFlip(self._angleCyclePos)

    self._angleCyclePos=(self._angleCyclePos+angle)%self._angleSize4
    newPhase = self.whatPhaseAngle(self._angleCyclePos)
    if (newPhase <> self._phase):
      self._phase = newPhase
      self._xCyclePos=self.stepFlip(self._xCyclePos)
      self._yCyclePos=self.stepFlip(self._yCyclePos)
    return self.returnLeftAndRightFromPosition()

  def returnLeftAndRightFromPosition(self):
    body = [self.stepPos(self._xCyclePos), self.stepPos(self._yCyclePos), self.anglePos(self._angleCyclePos)]
    bodyFlip = [self.inverseStepPos(self._xCyclePos), self.inverseStepPos(self._yCyclePos), self.inverseAnglePos(self._angleCyclePos)]
    left = body
    right = bodyFlip
    return left, self._phase, right, 1-self._phase
##    return left, right ##Body Leg x, y, angle, Left Leg x, y, angle, right leg x, y, angle

  def stepPos (self, position):
    stepPos0 = abs(position%self._stepLength4-self._stepLength2)-self._stepLength
    return stepPos0

  def inverseStepPos (self, position):
    return - self.stepPos(position)

  def anglePos (self, position):
    anglePos0 = abs(position%self._angleSize4-self._angleSize2)-self._angleSize
    return anglePos0

  def inverseAnglePos (self, position):
    anglePos0 = -1*self.anglePos(position)
    return anglePos0

  def stepPoss (self, position):
    stepPos0 = abs(position%self._stepLength4-self._stepLength2)-self._stepLength
    stepPos1 = -1*stepPos0
    return stepPos0, stepPos1

  def stepFlip (self, position):
    return (self._stepLength4 - position)%self._stepLength4
      
  def angleFlip (self, position):
    return (self._angleSize4 - position)%self._angleSize4
      
class TestStepMath(unittest.TestCase):

  def setUp(self):
    self.step=StepMath(10, 15, 5)

  def test_stepPos(self):
    self.assertEqual (self.step.stepPos(-10), 0)
    self.assertEqual (self.step.stepPos(-5), 5)
    self.assertEqual (self.step.stepPos(0), 10)
    self.assertEqual (self.step.stepPos(5), 5)
    self.assertEqual (self.step.stepPos(10), 0)
    self.assertEqual (self.step.stepPos(15), -5)
    self.assertEqual (self.step.stepPos(20), -10)
    self.assertEqual (self.step.stepPos(25), -5)
    self.assertEqual (self.step.stepPos(30), 0)
    self.assertEqual (self.step.stepPos(35), 5)
    self.assertEqual (self.step.stepPos(40), 10)
 
  def test_stepPoss(self):
    self.assertEqual (self.step.stepPoss(-10), (0, 0))
    self.assertEqual (self.step.stepPoss(-5), (5, -5))
    self.assertEqual (self.step.stepPoss(0), (10, -10))
    self.assertEqual (self.step.stepPoss(5), (5, -5))
    self.assertEqual (self.step.stepPoss(10), (0, 0))
    self.assertEqual (self.step.stepPoss(15), (-5, 5))
    self.assertEqual (self.step.stepPoss(20), (-10, 10))
    self.assertEqual (self.step.stepPoss(25), (-5, 5))
    self.assertEqual (self.step.stepPoss(30), (0, 0))
    self.assertEqual (self.step.stepPoss(35), (5, -5))
    self.assertEqual (self.step.stepPoss(40), (10, -10))
 
  def test_whatPhase(self):
    self.assertEqual (self.step.whatPhaseLength(0), 0)
    self.assertEqual (self.step.whatPhaseLength(5), 0)
    self.assertEqual (self.step.whatPhaseLength(10), 0)
    self.assertEqual (self.step.whatPhaseLength(15), 0)
    self.assertEqual (self.step.whatPhaseLength(20), 1)
    self.assertEqual (self.step.whatPhaseLength(25), 1)
    self.assertEqual (self.step.whatPhaseLength(30), 1)
    self.assertEqual (self.step.whatPhaseLength(35), 1)
    self.assertEqual (self.step.whatPhaseLength(40), 0)
    self.assertEqual (self.step.whatPhaseAngle(0), 0)
    self.assertEqual (self.step.whatPhaseAngle(5), 0)
    self.assertEqual (self.step.whatPhaseAngle(10), 0)
    self.assertEqual (self.step.whatPhaseAngle(15), 0)
    self.assertEqual (self.step.whatPhaseAngle(20), 0)
    self.assertEqual (self.step.whatPhaseAngle(25), 0)
    self.assertEqual (self.step.whatPhaseAngle(30), 1)
    self.assertEqual (self.step.whatPhaseAngle(35), 1)
    self.assertEqual (self.step.whatPhaseAngle(40), 1)
    self.assertEqual (self.step.whatPhaseAngle(45), 1)
    self.assertEqual (self.step.whatPhaseAngle(50), 1)
    self.assertEqual (self.step.whatPhaseAngle(55), 1)
    self.assertEqual (self.step.whatPhaseAngle(60), 0)

  def test_stepFlip(self):
    self.assertEqual (self.step.stepFlip(0), 0)
    self.assertEqual (self.step.stepFlip(5), 35)
    self.assertEqual (self.step.stepFlip(10), 30)
    self.assertEqual (self.step.stepFlip(15), 25)
    self.assertEqual (self.step.stepFlip(20), 20)
    self.assertEqual (self.step.stepFlip(25), 15)
    self.assertEqual (self.step.stepFlip(30), 10)
    self.assertEqual (self.step.stepFlip(35), 5)
    self.assertEqual (self.step.stepFlip(40), 0)
    self.assertEqual (self.step.stepFlip(-20), 20)
    self.assertEqual (self.step.stepFlip(-15), 15)
    self.assertEqual (self.step.stepFlip(-10), 10)
    self.assertEqual (self.step.stepFlip(-5), 5)

  def test_stepAllRelativeBodyPositionsFromStep(self):
    self.assertEqual (self.step.allRelativeBodyPositionsFromStep(0,0,0), ([[0, 0, 0], [0, 0, -5], [0, 0, 0], [0, 0, -5], [0, 0, 0], [0, 0, -5]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    self.assertEqual (self.step.allRelativeBodyPositionsFromStep(1,0,0), ([[-1, 0, 0], [1, 0, -5], [-1, 0, 0], [1, 0, -5], [-1, 0, 0], [1, 0, -5]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]))
    self.assertEqual (self.step.allRelativeBodyPositionsFromStep(-1,0,0), ([[0, 0, 0], [0, 0, -5], [0, 0, 0], [0, 0, -5], [0, 0, 0], [0, 0, -5]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]))
#    print self.step.allRelativeBodyPositionsFromStep(0,0,0)

  def test_stepRelativeBodyPositionsFromStep(self):
    self.assertEqual (self.step.relativeBodyPositionsFromStep(0,0,0), ([0, 0, 0], [0, 0, 0], [0, 0, -5], [0, 0, 0]))
    self.assertEqual (self.step.relativeBodyPositionsFromStep(1,0,0), ([-1, 0, 0], [0, 0, 0], [1, 0, -5], [0, 0, 0]))
    self.assertEqual (self.step.relativeBodyPositionsFromStep(-1,0,0), ([0, 0, 0], [0, 0, 0], [0, 0, -5], [0, 0, 0]))
#    print self.step.relativeBodyPositionsFromStep(0,0,0)

  def test_stepStep(self):
    self.assertEqual (self.step.relativeBodyPositionsFromTap(), ([0, 0, -5], [0, 0, 0], [0, 0, 0], [0, 0, 0]))
    self.assertEqual (self.step.relativeBodyPositionsFromTap(), ([0, 0, 0], [0, 0, 0], [0, 0, -5], [0, 0, 0]))
#    print self.step.relativeBodyPositionsFromTap()


if __name__ == '__main__':
  unittest.main()
    

    
