"""Motion"""

import time
import unittest
import legs
import stepMath
import vectorMath

class Animation:
    _initialised = False
    _sm = None
    _vm = None
    _legs = None
    _leg = []
    _legAngles = None

    def __init__(self, stepLength, angleSize, stepHeight):
        self._sm = stepMath.StepMath(stepLength, angleSize, stepHeight)
        self._vm = vectorMath.VectorMath()
        self._legs = legs.Legs()
        self._leg = self._legs.footPositions()
        self._legAngles = [0] * 6
        self._xAngleStepped = 0
        self._yAngleStepped = 0
        self._zDistanceStepped = 0

    def setInitialStance(self):
        self._legs.setInitialStance()

    def settleToInitialStance(self):
        for i in range(6):
            self._legs.settleToInitialStance(i)
        time.sleep(1)

    def settleToSleep(self):
##        for i in range(10):
##            self.step(0, 0, -1, 0, 0, 0)
##            time.sleep(0.1)
        self.settleToInitialStance()
        self._legs.setAllLegsToSamePosition(90, 120, 70)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(90, 90, 70)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(110, 70, 70)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(130, 60, 60)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(150, 50, 50)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(1)

    def raiseToInitialStance(self):
        self._legs.setAllLegsToSamePosition(90, 70, 50)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(90, 90, 50)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(90, 120, 50)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(90, 100, 70)
        time.sleep(0.1)
        self._legs._servos.stop()
        time.sleep(0.2)
        self._legs.setAllLegsToSamePosition(90, 90, 90)
        time.sleep(0.1)
        self._legs._servos.stop()

        self.settleToInitialStance()
        time.sleep(.1)
        self._legs._servos.stop()
        time.sleep(1)

    def _iterateToPosition(self, coxaAngle, femurAngle, tibiaAngle):
        currentLegPositions = self._legs.getLegAngles()
        targetLegPositions = [
            [coxaAngle, femurAngle, tibiaAngle],
            [coxaAngle, femurAngle, tibiaAngle],
            [coxaAngle, femurAngle, tibiaAngle],
            [coxaAngle, femurAngle, tibiaAngle],
            [coxaAngle, femurAngle, tibiaAngle],
            [coxaAngle, femurAngle, tibiaAngle]
            ]
        legPositionsDifference = self._vm.subLegVector(targetLegPositions, currentLegPositions)
        iterations = abs(self._vm.largestLegVectorComponent(legPositionsDifference))
        legPositionIteration = self._vm.scaleLegVector(legPositionsDifference, 1.0/iterations)
        for i in range(iterations):
            self._legs.setAllLegs(self._vm.addLegVector(currentLegPositions, self._vm.scaleLegVector(legPositionIteration, i)))
        self._legs.setAllLegsToSamePosition(coxaAngle, femurAngle, tibiaAngle)

    def step(self, xDistanceStepped, yDistanceStepped, zDistanceStepped, xAngleStepped, yAngleStepped, zAngleStepped):
#        print xDistanceStepped, yDistanceStepped, zAngleStepped
        bodyRotation = [0, 0, 0]
        bodyPosition = [0, 0, 0]

        #Step x, y and rotation around z-axis
        bodyPosition, bodyRotation = self._sm.allRelativeBodyPositionsFromStep(xDistanceStepped, yDistanceStepped, zAngleStepped)

        ##relativeBodyPositionsFromStep only calculates x distance, y distance, and rotation around z-axis as those are used for walking.
        ##Rotation around x and y, and z-axis distance, can be used for posing while walking.
        ##Add in torso rotation, height here, eventually

        self._xAngleStepped = self._xAngleStepped + xAngleStepped
        if self._xAngleStepped > 10:
            self._xAngleStepped = 10
        if self._xAngleStepped < -10:
            self._xAngleStepped = -10
        self._yAngleStepped = self._yAngleStepped + yAngleStepped
        if self._yAngleStepped > 10:
            self._yAngleStepped = 10
        if self._yAngleStepped < -10:
            self._yAngleStepped = -10
        self._zDistanceStepped = self._zDistanceStepped + zDistanceStepped
        if self._zDistanceStepped > 10:
            self._zDistanceStepped = 10
        if self._zDistanceStepped < -10:
            self._zDistanceStepped = -10

#        print bodyPosition[2]
#        bodyRotation[0] = self._xAngleStepped
#        bodyRotation[1] = self._yAngleStepped
#        bodyPosition[2] = bodyPosition[2] + self._zDistanceStepped

        for i in range(0, 6):
            #Add rotation and height
            bodyRotation[i][0] = bodyRotation[i][0] + self._xAngleStepped
            bodyRotation[i][1] = bodyRotation[i][1] + self._yAngleStepped
            bodyPosition[i][2] = bodyPosition[i][2] + self._zDistanceStepped
            #calculate the angles
            self._legAngles[i] = self._leg[i].calcIKFootPosition(bodyPosition[i], bodyRotation[i])
        #set servos to that position
        self._legs.setAllLegs(self._legAngles)

class TestAnimation(unittest.TestCase):

    def setUp(self):
        self.ani = Animation(30, 10, 20)

    #def test_animation_setup(self):
    #    self.ani.raiseToInitialStance()
    #    time.sleep(3)
    #    self.ani.settleToSleep()
    #    time.sleep(1)       
    #    self.ani._legs._servos.end()
       
    def test_animation_iterate(self):
        self.ani._legs.setAllLegsToSamePosition(90, 90, 90)
        self.ani._iterateToPosition(90, 100, 110)
        self.ani._iterateToPosition(90, 90, 120)
        print()
   
if __name__ == '__main__':
    unittest.main()
