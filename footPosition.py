import mathLookup
import vectorMath
import stubbyIK
import unittest

class FootPosition:

    _mathLookup = mathLookup.MathLookup()
    _vectorMath = vectorMath.VectorMath()

    def __init__(self, sideLengthOfHex, coxaRotation, coxaLength, femurLength, tibiaLength, femurAngle, tibiaAngle):
        self._sideLengthOfHex = sideLengthOfHex
        self._coxaRotation = coxaRotation
        self._coxaLength = coxaLength
        self._femurLength = femurLength
        self._tibiaLength = tibiaLength
        self._initialCoxaPosition = self.calcCoxaBodyPosition(sideLengthOfHex, coxaRotation)
        self._initialFootPosition = self.calcInitialFootPosition(coxaRotation, femurAngle, tibiaAngle)
        self._initialCoxaRotation = coxaRotation
        self._ik = stubbyIK.StubbyIK(coxaLength, femurLength, tibiaLength)

    def __str__(self):
        return "member of footPosition for Coxa Position {0}".format(self._coxaRotation)

    def calcCoxaBodyPosition(self, lengthToPosition, rotation):
        return self._vectorMath.rotate([0, lengthToPosition, 0], 0, 0, rotation)

    def calcInitialFootPosition(self, rotation, femurAngle, tibiaAngle):
        initialLegLengthX = 0
        initialLegLengthY = int(self._sideLengthOfHex + self._coxaLength + self._femurLength * self._mathLookup.sin(femurAngle) + self._tibiaLength * self._mathLookup.sin(femurAngle+tibiaAngle-180))
        initialLegLengthZ = -int(self._femurLength * self._mathLookup.cos(femurAngle) + self._tibiaLength * self._mathLookup.cos(femurAngle+tibiaAngle-180))
        footPosition = [initialLegLengthX, initialLegLengthY, initialLegLengthZ]
        return self._vectorMath.rotate(footPosition, 0, 0, rotation)

    def calcFKFootPosition(self, vecOffset, vecRotate, coxaAngle, femurAngle, tibiaAngle):
        return self._ik.calcFKFootPosition(self._initialCoxaPosition, vecOffset, vecRotate, coxaAngle, femurAngle, tibiaAngle)

    def calcIKFootPosition(self, vecOffset, vecRotate):
        legAngles, xyMagnitude = self._ik.calcIKFootPosition(self._initialCoxaPosition, vecOffset, vecRotate, self._initialFootPosition)
        legAngles[0] = (legAngles[0] - self._initialCoxaRotation)%360
        return legAngles, xyMagnitude

class TestFootPosition(unittest.TestCase):

    def setUp(self):
        self.v = vectorMath.VectorMath()
        self.m = mathLookup.MathLookup()
        self.sideLengthOfHex = 50
        self.coxaRotation = 0
        self.coxaLength = 20
        self.femurLength = 40
        self.tibiaLength = 80
        self.femurAngle = 90
        self.tibiaAngle = 90
        self.footPosition = FootPosition(self.sideLengthOfHex, self.coxaRotation, self.coxaLength, self.femurLength, self.tibiaLength, self.femurAngle, self.tibiaAngle)

    def test_calcCoxaBodyPosition(self):
        for angle in range(0, 361):
            self.assertTrue(self.v.almostEqual(self.footPosition.calcCoxaBodyPosition(self.sideLengthOfHex, angle), [self.sideLengthOfHex * -self.m.sin(angle), self.sideLengthOfHex * self.m.cos(angle), 0]))

    def test_calcInitialFootPosition(self):
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(0, 90, 90), [0, 110, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(0, 90, 0), [0, 30, 0]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(0, 90, 180), [0, 190, 0]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(0, 150, 60), [0, 130, -34]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(0, 0, 180), [0, 70, -120]))

        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(0, 90, 90), [0, 110, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(90, 90, 90), [-110, 0, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(180, 90, 90), [0, -110, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(270, 90, 90), [110, 0, -80]))
        for angle in range(0, 361):
            self.assertTrue(self.v.almostEqual(self.footPosition.calcInitialFootPosition(angle, 90, 90), [110 * -self.m.sin(angle), 110 * self.m.cos(angle), -80]))

    def test_calcFKFootPosition(self):
        self.assertTrue(self.v.almostEqual(self.footPosition.calcFKFootPosition([0, 0, 0], [0, 0, 0], 90, 90, 90), [0, 110, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcFKFootPosition([100, 0, 0], [0, 0, 0], 90, 90, 90), [100, 110, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcFKFootPosition([0, 100, 0], [0, 0, 0], 90, 90, 90), [0, 210, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcFKFootPosition([0, 0, 100], [0, 0, 0], 90, 90, 90), [0, 110, 20]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcFKFootPosition([0, 0, 0], [0, 0, 0], 0, 90, 90), [60, 50, -80]))
        self.assertTrue(self.v.almostEqual(self.footPosition.calcFKFootPosition([0, 0, 0], [0, 0, 0], 180, 90, 90), [-60, 50, -80]))

    def test_calcIKFootPosition(self):
        position, magnitude = self.footPosition.calcIKFootPosition([0, 0, 0], [0, 0, 0])
        self.assertTrue(self.v.almostEqualAngle(position, [90, 90, 90]))
        self.assertEqual(magnitude, 0.0)
        ##print self.footPosition.calcIKFootPosition([0, 0, 0], [0, 0, 10])
        ##print self.footPosition.calcIKFootPosition([0, 0, 0], [0, 0, 20])

if __name__ == '__main__':
    unittest.main()
