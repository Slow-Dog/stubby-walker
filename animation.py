"""Motion"""

import time
import unittest
import legs
import stepMath

class Animation:
    _initialised = False
    _sm = None
    _legs = None
    _leg = []
    _legAngles = None

    def __init__(self, stepLength, angleSize, stepHeight):
        self._sm = stepMath.StepMath(stepLength, angleSize, stepHeight)
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

if __name__ == '__main__':
    unittest.main()
