import math
import unittest
from array import *

class MathLookup:

    _initialised = False
    _cosLookup = array('f')
    _sinLookup = array('f')
    _sqrtLookup = array('f')
    _asinLookup = array('f')
    _acosLookup = array('f')
    #_cosLookup = []
    #_sinLookup = []
    #_sqrtLookup = []
    #_asinLookup = []
    #_acosLookup = []
    _sqrtRange = 10000
    _pi180 = math.pi/180

    def __init__(self):
        if not MathLookup._initialised:
            MathLookup._initialised = True
            #set up lookups for cos and sin
            for x in range(0, 360):
                MathLookup._cosLookup.append(math.cos(float(x)/180.0*math.pi))
                MathLookup._sinLookup.append(math.sin(float(x)/180.0*math.pi))

            #set up lookups for square roots
            for x in range(0, MathLookup._sqrtRange):
                MathLookup._sqrtLookup.append(int(round(math.sqrt(x))))

            #set up lookups for inverse cos and inverse sin
            for x in range(0, 2000):
                a = (x/1000.0)-1
                r = math.asin(a)/self._pi180
                MathLookup._asinLookup.append(int(r))
                r = math.acos(a)/self._pi180
                MathLookup._acosLookup.append(int(r))

        self.piOver4 = math.pi/4
        
    def cos(self, a):
#        return math.cos(a*self._pi180)
        x = (int(a))%360
        return MathLookup._cosLookup[x]

    def mathCos(self, a):
        return math.cos(a*math.pi/180)

    def sin(self, a):
#        return math.sin(a*self._pi180)
        x = (int(a))%360
        return MathLookup._sinLookup[x]

    def mathSin(self, a):
        return math.sin(a*math.pi/180)

    def sqrt(self, a):
#        return math.sqrt(a)
        x = int(a)
        if x < MathLookup._sqrtRange:
            return MathLookup._sqrtLookup[x]
        return math.sqrt(x)

    def asin(self, a):
        if a >= -1 and a < 1:
            x = int((a+1)*1000)
            return MathLookup._asinLookup[x]
        return 0
            
    def acos(self, a):
        if a >= -1 and a < 1:
            x = int((a+1)*1000)
            return MathLookup._acosLookup[x]
        return 0

    def mathAcos(self, a):
        if a >= -1 and a < 1:
            return math.acos(a)/math.pi*180.0
        return 0
    
    def atan2(self, y, x):
        return self.mathAtan2(y, x)
        ##"Fast" atan approximation actually slower in practice
        ##a = min (x, y) / max (x, y)
        ##s = a * a
        ##r = ((-0.0464964749 * s + 0.15931422) * s - 0.327622764) * s * a + a
        ##if y > x:
        ##    r = 1.57079637 - r
        ##if x < 0:
        ##    r = 3.14159274 - r
        ##if y < 0:
        ##    r = -r
        ##return r/math.pi*180

    def mathAtan2(self, y, x):
        return math.atan2(y, x)/math.pi*180.0
    
    def mathCosineRuleAngle(self, adjSideA, adjSideB, oppSide):
        if oppSide >= adjSideA + adjSideB:
            return 180        
        if adjSideA == 0 or adjSideB == 0:
            return 0
        return self.mathAcos((adjSideA*adjSideA +adjSideB*adjSideB-oppSide*oppSide)/(2.0*adjSideA*adjSideB))

    def cosineRuleAngle(self, adjSideA, adjSideB, oppSide):
        if oppSide >= adjSideA + adjSideB:
            return 180        
        if adjSideA == 0 or adjSideB == 0:
            return 0
        return self.acos((adjSideA*adjSideA +adjSideB*adjSideB-oppSide*oppSide)/(2.0*adjSideA*adjSideB))

    def mathCosineRuleLength(self, sideA, sideB, oppAngle):
        return math.sqrt(sideA*sideA+sideB*sideB-2.0*sideA*sideB*math.cos(oppAngle/180.0*math.pi))

    def cosineRuleLength(self, sideA, sideB, oppAngle):
        return self.sqrt(sideA*sideA+sideB*sideB-2.0*sideA*sideB*self.cos(oppAngle))

class TestMathLookup(unittest.TestCase):
 
    def setUp(self):
        self.m = MathLookup()         
 
    def test_cos(self):
        for a in range(0, 360):
            self.assertTrue(self.m.cos(a) - self.m.mathCos(a) < 0.0001, "Failed for Cos " + str(a) + ": " + str(self.m.cos(a)) + ", " + str(self.m.mathCos(a)))
        for a in range(-500, 500, 20):
            self.assertTrue(self.m.cos(a) - self.m.mathCos(a) < 0.0001, "Failed for Cos " + str(a) + ": " + str(self.m.cos(a)) + ", " + str(self.m.mathCos(a)))
 
    def test_sin(self):
        for a in range(0, 360):
            self.assertTrue(self.m.sin(a) - self.m.mathSin(a) < 0.0001, "Failed for Sin " + str(a) + ": " + str(self.m.sin(a)) + ", " + str(self.m.mathSin(a)))
        for a in range(-500, 500, 20):
            self.assertTrue(self.m.sin(a) - self.m.mathSin(a) < 0.0001, "Failed for Sin " + str(a) + ": " + str(self.m.sin(a)) + ", " + str(self.m.mathSin(a)))

    def test_atan2(self):
        self.assertTrue(self.m.atan2(10, 10) - self.m.mathAtan2(10, 10) < 0.0001)

    def test_cosineRuleLength(self):
        self.assertEqual(round(self.m.cosineRuleLength(100, 100, 60)), 100)
        self.assertEqual(round(self.m.cosineRuleLength(200, 200, 60)), 200)
        self.assertEqual(round(self.m.cosineRuleLength(100, 100, 120)), 173)
        self.assertEqual(round(self.m.cosineRuleLength(100, 50, 60)), round(self.m.cosineRuleLength(50, 100, 60)))

    def test_cosineRuleAngle(self):
        self.assertEqual(round(self.m.cosineRuleAngle(100, 100, 100)), 60)
        self.assertEqual(round(self.m.cosineRuleAngle(200, 200, 200)), 60)
        self.assertEqual(round(self.m.cosineRuleAngle(100, 100, 174)), 120)
        self.assertEqual(round(self.m.cosineRuleAngle(0, 100, 100)), 180)
        self.assertEqual(round(self.m.cosineRuleAngle(0, 100, 50)), 0)
        self.assertEqual(round(self.m.cosineRuleAngle(100, 50, 100)), round(self.m.cosineRuleAngle(50, 100, 100)))

if __name__ == '__main__':
    unittest.main()
