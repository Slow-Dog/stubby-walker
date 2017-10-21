from json import JSONEncoder
import unittest

class StubbyData(JSONEncoder):

    #servo pin numbers
    servos = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    #servo pin numbers for each leg [coxa, femur, tibia] joints
    legServoPins = [[12, 8, 9], [5, 4, 17], [7, 14, 3], [18, 16, 19], [15, 13, 6], [2, 10, 11]]

    #neutral offset. Pulswidth to add to get joint to zero
    #vagaries of construction mean that each joint's (really, the servo's) zero position isn't exact. This offset is added to the calculted angle to position each properly.
    #found by programmatically setting the robot leg positions to 90 degress and measuring
    _neutral = [0, 0, 0, -90, 0,
                0, 55, 0, -33, 0,
                0, -55, -55, 0, 0,
                55, -33, 0, 110, 55]

    def default(self, o):
        return o.__dict__    

class TestStubbyData(unittest.TestCase):

    def setUp(self):
        self.s = StubbyData() 

if __name__ == '__main__':
    unittest.main()
