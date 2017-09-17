
import math
import mathLookup
import vectorMathLookup
import unittest

class StubbyIK:

  _m = mathLookup.MathLookup()
  _v = vectorMathLookup.VectorMathLookup()

  def __init__(self, coxaLength, femurLength, tibiaLength):
    self._coxaLength = coxaLength
    self._femurLength= femurLength
    self._tibiaLength = tibiaLength

  ##Calculates the 3D position of the foot given a body rotation, offset and set of joint angles.
  def calcFKFootPosition(self, initialCoxaPosition, vecOffset, vecRotate, coxaAngle, femurAngle, tibiaAngle):
    #leg
    legLengthX =  0
    legLengthY =  int(self._coxaLength + self._femurLength * self._m.sin(femurAngle) + self._tibiaLength * self._m.sin(femurAngle+tibiaAngle-180))
    legLengthZ =                    -int(self._femurLength * self._m.cos(femurAngle) + self._tibiaLength * self._m.cos(femurAngle+tibiaAngle-180))
    footPosition = [legLengthX, legLengthY, legLengthZ]
    footPosition = self._v.rotate(footPosition, 0, 0, (coxaAngle - 90))

    ##Add in initial Coxa Position offset
    footPosition = self._v.addVector(footPosition, initialCoxaPosition)
    
    ##Rotate and translate Coxa Position

    ##Each axis rotation
    footPosition = self._v.rotate(footPosition, vecRotate[0], vecRotate[1], vecRotate[2])

    #add current body translation
    footPosition = self._v.addVector(footPosition, vecOffset)

    return footPosition

  ##Calculates the joint angles required to position the body at a given rotation and offset from the initial foot position
  def calcIKFootPosition(self, initialCoxaPosition, vecOffset, vecRotate, initialFootPosition):
    ##Rotate and translate initial Coxa Positions to desired body position

    #Each axis rotation
    newFootPosition = self._v.rotate(initialFootPosition, -vecRotate[0], -vecRotate[1], -vecRotate[2])

    #add current body translation
    newFootPosition = self._v.subVector(newFootPosition, vecOffset)

    #calculate leg angles from body position to target
    return self.calcLegAngles(initialCoxaPosition, newFootPosition)


  ##Calculates the joint angles required to bridge from one position to another
  def calcLegAngles (self, startPosition, targetPosition):
    ##subtract startposition
    targetFootPos = self._v.subVector(targetPosition, startPosition)
    
    coxaAngle = (int(round(math.atan2(targetFootPos[1], targetFootPos[0])/math.pi*180)))%360

    coxaLength = self._coxaLength
    legDistance = self._m.sqrt(targetFootPos[0]*targetFootPos[0]+targetFootPos[1]*targetFootPos[1])-self._coxaLength
    legHeight = int(targetFootPos[2])
    legExtent = self._m.sqrt(legDistance*legDistance + legHeight*legHeight)

    theta1 = (int(round(math.atan2(legHeight, legDistance)/math.pi*180))+90)%360
    theta2 = self._m.cosineRuleAngle(self._femurLength, legExtent, self._tibiaLength)
    phi = self._m.cosineRuleAngle(self._tibiaLength, self._femurLength, legExtent)

#    print theta1, theta2, phi
    return [int(coxaAngle), int((theta1+theta2)), int(phi)]

class TeststubbyIK(unittest.TestCase):

  def setUp(self):
    self.v=vectorMathLookup.VectorMathLookup()
    self.m = mathLookup.MathLookup()
    self.coxaLength = 20
    self.femurLength= 40
    self.tibiaLength = 80

    self.ik=StubbyIK(self.coxaLength, self.femurLength, self.tibiaLength)

    self.nobodyik=StubbyIK(0, 100, 100)

  def test_calcFKFootPosition(self):
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,0], 90, 90, 90), [0, 110, -80]))
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [100,0,0], [0,0,0], 90, 90, 90), [100, 110, -80]))
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,100,0], [0,0,0], 90, 90, 90), [0, 210, -80]))
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,100], [0,0,0], 90, 90, 90), [0, 110, 20]))

    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,0], 0, 90, 90), [60, 50, -80]))
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,0], 180, 90, 90), [-60, 50, -80]))

    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,90], 90, 90, 90), [-110, 0, -80]))
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,180], 90, 90, 90), [0, -110, -80]))
    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,270], 90, 90, 90), [110, 0, -80]))

    self.assertTrue (self.v.almostEqual(self.ik.calcFKFootPosition([0,50,0], [0,0,0], [0,0,90], 0, 90, 90), [-50, 60, -80]))

 
  def test_calcLegAngles(self):
    self.assertTrue (self.v.almostEqualAngle (self.nobodyik.calcLegAngles([0, 0, 0], [0, 200, 0]), [90, 90, 180]))
    self.assertTrue (self.v.almostEqualAngle (self.nobodyik.calcLegAngles([0, 0, 0], [0, 100, 0]), [90, 150, 60]))
    self.assertTrue (self.v.almostEqualAngle (self.nobodyik.calcLegAngles([0, 0, 0], [0, 50, -86]), [90, 90, 60]))
    
##    self.assertTrue (self.v.almostEqualAngle (self.ik.calcLegAngles(self.ik.calcCoxaBodyPosition(self.sideLengthOfHex, 0), [0, 110, -80]), [90, 90, 90]))
##    self.assertTrue (self.v.almostEqualAngle (self.ik.calcLegAngles(self.ik.calcCoxaBodyPosition(self.sideLengthOfHex, 0), [60, 50, -80]), [0, 90, 90]))
##    self.assertTrue (self.v.almostEqualAngle (self.ik.calcLegAngles(self.ik.calcCoxaBodyPosition(self.sideLengthOfHex, 0), [-60, 50, -80]), [180, 90, 90]))
    

  def test_calcIKFootPosition(self):
    self.assertTrue (self.v.almostEqualAngle (self.ik.calcIKFootPosition([0,50,0], [0,0,0], [0,0,0], [0, 110, -80]), [90, 90, 90]))
##    print self.ik.calcIKFootPosition([0,0,0], [0,0,30])
##    print self.ik.calcFKFootPosition([0,0,0], [0,0,30], 69, 89, -79)
    
if __name__ == '__main__':
    unittest.main()
    

    
