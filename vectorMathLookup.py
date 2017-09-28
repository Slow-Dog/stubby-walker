import math
import mathLookup
import unittest

class VectorMathLookup:

  def __init__(self):
    self.data = []
    self.m = mathLookup.MathLookup()
    
  #rotate ([x,y,z], angleA, angleB, angleC)
  def rotate(self, point, angleA, angleB, angleC):
    x=point[0]
    y=point[1]
    z=point[2]
    cosA=self.m.cos(angleA)
    sinA=self.m.sin(angleA)
    cosB=self.m.cos(angleB)
    sinB=self.m.sin(angleB)
    cosC=self.m.cos(angleC)
    sinC=self.m.sin(angleC)
    #rotate around x then y then z
    outX = x*(cosB*cosC)+y*(cosC*sinA*sinB-cosA*sinC)+z*(cosA*cosC*sinB+sinA*sinC)
    outY = x*(cosB*sinC)+y*(cosA*cosC+sinA*sinB*sinC)+z*(-cosC*sinA+cosA*sinB*sinC)
    outZ = x*(-sinB)+y*(sinA*cosB)+z*(cosA*cosB)
##    #rotate around z then y then x
##    outX = x*(cosB*cosC)+y*(-cosB*sinC)+z*(sinB)
##    outY = x*(cosA*sinC+sinA*sinB*cosC)+y*(cosA*cosC-sinA*sinB*sinC)+z*(-sinA*cosB)
##    outZ = x*(sinA*sinC-cosA*sinB*cosC)+y*(sinA*cosC+cosA*sinB*sinC)+z*(cosA*cosB)
    return [outX, outY, outZ]

  def addVector(self, x, y):
    r = []
    for a, b in zip(x, y):
      r.append(a+b)
    return r

  def subVector(self, x, y):
    r = []
    for a, b in zip(x, y):
      r.append(a-b)
    return r

  def magnitude(self, x):
    r = 0
    for a in x:
      r=r+(a*a)
    return self.m.sqrt(r)

  def almostEqual(self, x, y):
    r = True
    for a, b in zip(x, y):
      if (abs(a - b) > 0.00001):
        r = False
    return r
  
  def almostEqualAngle(self, x, y):
    r = True
    for a, b in zip(x, y):
      if (abs(int(a) - int(b)) > 1):
        r = False
    return r
  

class TestVectorMathLookup(unittest.TestCase):
 
  def setUp(self):
    self.v=VectorMathLookup()
    self.m = mathLookup.MathLookup()

  def test_almostEqual(self):
    self.assertTrue(self.v.almostEqual([1], [1]))
    self.assertTrue(self.v.almostEqual([0], [0]))
    self.assertTrue(self.v.almostEqual([-1], [-1]))
    self.assertTrue(self.v.almostEqual([1], [1.000001]))
    self.assertTrue(self.v.almostEqual([1], [0.999999]))
    self.assertTrue(self.v.almostEqual([0.0], [0.0]))
    self.assertTrue(self.v.almostEqual([0], [0.0]))
    self.assertTrue(self.v.almostEqual([0.0], [-0.0]))

    self.assertFalse(self.v.almostEqual([1], [3]))
    self.assertFalse(self.v.almostEqual([1], [-1]))
    self.assertFalse(self.v.almostEqual([1], [0]))
    self.assertFalse(self.v.almostEqual([0], [-100]))
    self.assertFalse(self.v.almostEqual([-100], [0]))
    self.assertFalse(self.v.almostEqual([-100], [100]))

  def almostEqualAngle(self):
    self.assertTrue(self.v.almostEqualAngle([1], [1]))
    self.assertTrue(self.v.almostEqualAngle([0], [0]))
    self.assertTrue(self.v.almostEqualAngle([-1], [-1]))
    self.assertTrue(self.v.almostEqualAngle([1], [2]))
    self.assertTrue(self.v.almostEqualAngle([1], [0]))

    self.assertFalse(self.v.almostEqualAngle([1], [1.001]))
    self.assertFalse(self.v.almostEqualAngle([1], [0.999]))
    self.assertFalse(self.v.almostEqualAngle([1], [0]))
    self.assertFalse(self.v.almostEqualAngle([1], [-1]))
    self.assertFalse(self.v.almostEqualAngle([-1], [0]))
    self.assertFalse(self.v.almostEqualAngle([-1], [1]))
 
  def test_addVector(self):
    a = [1, 2, 3]
    b = [3, 2, 1]
    c = [-1, -2 , -3]
    self.assertEqual (self.v.addVector(a, a), [2, 4, 6])
    self.assertEqual (self.v.addVector(a, b), [4, 4, 4])
    self.assertEqual (self.v.addVector(a, c), [0, 0, 0])
    self.assertEqual (self.v.addVector(b, a), [4, 4, 4])
    self.assertEqual (self.v.addVector(b, b), [6, 4, 2])
    self.assertEqual (self.v.addVector(b, c), [2, 0, -2])
    self.assertEqual (self.v.addVector(c, a), [0, 0, 0])
    self.assertEqual (self.v.addVector(c, b), [2, 0, -2])
    self.assertEqual (self.v.addVector(c, c), [-2, -4, -6])
 
  def test_subVector(self):
    a = [1, 2, 3]
    b = [3, 2, 1]
    c = [-1, -2 , -3]
    self.assertEqual (self.v.subVector(a, a), [0, 0, 0])
    self.assertEqual (self.v.subVector(a, b), [-2, 0, 2])
    self.assertEqual (self.v.subVector(a, c), [2, 4, 6])
    self.assertEqual (self.v.subVector(b, a), [2, 0, -2])
    self.assertEqual (self.v.subVector(b, b), [0, 0, 0])
    self.assertEqual (self.v.subVector(b, c), [4, 4, 4])
    self.assertEqual (self.v.subVector(c, a), [-2, -4, -6])
    self.assertEqual (self.v.subVector(c, b), [-4, -4, -4])
    self.assertEqual (self.v.subVector(c, c), [0, 0, 0])
 
  def test_magnitude(self):
    self.assertEqual (self.v.magnitude([0]), 0)
    self.assertEqual (self.v.magnitude([1,2,2]), 3)
    self.assertEqual (self.v.magnitude([2,2,2,2]), 4)
    self.assertEqual (self.v.magnitude([1,2,-2]), 3)
    self.assertEqual (self.v.magnitude([2,-2,2,2]), 4)
 
  def test_rotate(self):
    a = [100, 0, 0]
    b = [0, 100, 0]
    c = [0, 0, 100]
    self.assertTrue (self.v.almostEqual(self.v.rotate(a, 0, 0, 0), a))
    self.assertTrue (self.v.almostEqual(self.v.rotate(b, 0, 0, 0), b))
    self.assertTrue (self.v.almostEqual(self.v.rotate(c, 0, 0, 0), c))
    
    self.assertTrue (self.v.almostEqual(self.v.rotate(a, 90, 0, 0), a))
    self.assertTrue (self.v.almostEqual(self.v.rotate(b, 90, 0, 0), [0, 0, 100]))
    self.assertTrue (self.v.almostEqual(self.v.rotate(c, 90, 0, 0), [0, -100, 0]))
    
    self.assertTrue (self.v.almostEqual(self.v.rotate(a, 0, 90, 0), [0, 0, -100]))
    self.assertTrue (self.v.almostEqual(self.v.rotate(b, 0, 90, 0), b))
    self.assertTrue (self.v.almostEqual(self.v.rotate(c, 0, 90, 0), [100, 0, 0]))

    self.assertTrue (self.v.almostEqual(self.v.rotate(a, 0, 0, 90), [0, 100, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate(b, 0, 0, 90), [-100, 0, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate(c, 0, 0, 90), c))

    self.assertTrue (self.v.almostEqual(self.v.rotate([100, 0, 0], 0, 0, 0), [100, 0, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate([100, 0, 0], 0, 0, 90), [0, 100, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate([100, 0, 0], 0, 0, 180), [-100, 0, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate([100, 0, 0], 0, 0, 270), [0, -100, 0]))

    self.assertTrue (self.v.almostEqual(self.v.rotate([0, 100, 0], 0, 0, 0), [0, 100, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate([0, 100, 0], 0, 0, 90), [-100, 0, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate([0, 100, 0], 0, 0, 180), [0, -100, 0]))
    self.assertTrue (self.v.almostEqual(self.v.rotate([0, 100, 0], 0, 0, 270), [100, 0, 0]))

    for angle in range (0, 361):
      self.assertTrue (self.v.almostEqual(self.v.rotate(c, angle, 0, 0), [0, 100 * -self.m.sin(angle), 100 * self.m.cos(angle)]), "Rotate around X for angle " + str(angle))
      self.assertTrue (self.v.almostEqual(self.v.rotate(a, 0, angle, 0), [100 * self.m.cos(angle), 0, 100 * -self.m.sin(angle)]), "Rotate around Y for angle " + str(angle))
      self.assertTrue (self.v.almostEqual(self.v.rotate(b, 0, 0, angle), [100 * -self.m.sin(angle), 100 * self.m.cos(angle), 0]), "Rotate around Z for angle " + str(angle))

if __name__ == '__main__':
    unittest.main()