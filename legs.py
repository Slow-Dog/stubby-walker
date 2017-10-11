from array import *
import unittest
import mathLookup
import footPosition
import servos
import time

class Legs:

    #servo pin numbers for each leg [coxa, femur, tibia] joints
    legServoPins = [[12, 8, 9], [5, 4, 17], [7, 14, 3], [18, 16, 19], [15, 13, 6], [2, 10, 11]]

    #neutral offset. Angle to add when set to 0 to get joint to zero
    #vagaries of construction mean that each joint's zero position isn't exact. This offset is added to the calculted angle to position each properly.
    #found by programmatically setting the robot leg positions to zero and measuring
    neutral = [[0, -10, -7], [-0, -15, -5], [-0, -10, -10], [-10, 10, 0], [0, -5, 0], [-10, -10, -5]]

    ##Dimension in mm or degrees
    ##Hexapod Dimensions
    ##
    ## Top View
    ##
    ##         coxaLength. From joint at body to position of femur joint
    ##     \   |
    ##      \_ V
    ## _ _ _/ \_ _ _
    ##      \_/
    ##      / \
    ##     /   \
    ##    /  ^  \
    ##       |
    ##       sideLengthOfHex
    ##
    ##
    ## Coxa  Femur
    ##     |     |
    ##     V     V
    ##  _ _ __ _ _ 
    ## /   |__|   \ <- Tibia
    ##
    ##


    sideLengthOfHex = 47
    coxaLength = 53
    femurLength = 40
    tibiaLength = 58

    coxaRotationDirection = 1

    ## For a simple joint the leg is connected to the servo and rotates the joint directly.
    ## Set complx<joint> to False
    ##
    ## A complex joint uses a pushrod connected to a servo horn to move the joint indirectly
    ## This is labelling:
    ##
    ##          Clength
    ##         *------.---0
    ## Dlength|      /
    ##       |      / Blength (Pushrod)
    ##     [O]-----o
    ##          Alength (Servo horn)                 
    ##
    ## Note all lengths are measured between pivot points and joints.
    ## Thus the Femur Length is from the Femur joint to Tibia Joint, 
    ## while the FemurCLength is from the Femur joint to where the pushrod is connected to the femur

    complexFemur = True
    femurAlength = 15
    femurBlength = 55
    femurClength = 35
    femurDlength = 26

    ## The basic calculations assume the angle * in the above diagram is 90 degrees
    ## i.e. that the joint is above the servo.
    ## If it isn't, then the offset angle is the amount more that 90 degrees
    femurOffsetAngle = 35

    ## If your servo is mounted the opposite way to mine,
    ## and the joint contracts when it should expand,
    ## set this to -1
    ## Valid for simple and complex joints
    femurRotationDirection = 1

    ## Same again for Tibia
    complexTibia = True
    tibiaAlength = 17
    tibiaBlength = 41
    tibiaClength = 35
    tibiaDlength = 29
    tibiaOffsetAngle = 25
    tibiaRotationDirection = 1

    ## And again for Coxa
    complexCoxa = False
    coxaAlength = 0
    coxaBlength = 0
    coxaClength = 0
    coxaDlength = 0
    coxaOffsetAngle = 0
    coxaRotationDirection = 1

    #Define initial stance
    #Use internal angles, where 0 = folded, 180 is open
    stanceCoxaAngle = 90
    stanceFemurAngle = 60
    stanceTibiaAngle = 110

    #height of femur joint over robot centre
    femurJointHeight = 35.0

    ## The above values are used to form lookup tables.
    ## The live calculations determine leg joint angles,
    ## and these lookups calculate servo settings for the joint angle.

    servoLookupCoxa = array('i')
    servoLookupFemur = array('i')
    servoLookupTibia = array('i')
    #servoLookupCoxa = []
    #servoLookupFemur = []
    #servoLookupTibia = []

    ##Holds each foot position
    footPosition = []

    _mathLookup = mathLookup.MathLookup()
    _servos = servos.Servos()

    def __init__(self):
        for a in range (0, 360):
            Legs.servoLookupCoxa.append(int ((a-90)/90.0*1000.0*Legs.coxaRotationDirection)+1500)

            if Legs.complexFemur:
                e1 = Legs._mathLookup.mathCosineRuleLength(Legs.femurClength, Legs.femurDlength, a+Legs.femurOffsetAngle)
                if (e1 < Legs.femurBlength+Legs.femurAlength) and (e1 > Legs.femurBlength-Legs.femurAlength):
                    a1 = Legs._mathLookup.mathCosineRuleAngle(e1, Legs.femurDlength, Legs.femurClength)
                    a2 = Legs._mathLookup.mathCosineRuleAngle(e1, Legs.femurAlength, Legs.femurBlength)
                    Legs.servoLookupFemur.append(int((a1+a2-90)/90*1000*Legs.femurRotationDirection)+1500)
                else:
                    a1 = 0
                    a2 = 0
                    Legs.servoLookupFemur.append(0)
            else:
                Legs.servoLookupFemur.append(int((a-90)/90.0*1000.0*Legs.femurRotationDirection)+1500)

            if Legs.complexTibia:
                e2 = Legs._mathLookup.mathCosineRuleLength(Legs.tibiaClength, Legs.tibiaDlength, a+Legs.tibiaOffsetAngle)
                if (e2 < Legs.tibiaBlength+Legs.tibiaAlength) and (e1 > Legs.tibiaBlength-Legs.tibiaAlength):
                    a3 = Legs._mathLookup.mathCosineRuleAngle(e2, Legs.tibiaDlength, Legs.tibiaClength)
                    a4 = Legs._mathLookup.mathCosineRuleAngle(e2, Legs.tibiaAlength, Legs.tibiaBlength)
                    Legs.servoLookupTibia.append(int((a3+a4-90)/90*1000*Legs.tibiaRotationDirection)+1500)
                else:
                    a3 = 0
                    a4 = 0
                    Legs.servoLookupTibia.append(0)
            else:
                Legs.servoLookupTibia.append(int ((a-90)/90.0*1000.0*Legs.tibiaRotationDirection)+1500)

        ##rotate around to define each initial position of each foot for a coxa angle
        ##If your Hexapod isn't rotationally symmetrical, set them manually
        for i in range(0, 6):
            thisCoxaRotation = i*60-30
            Legs.footPosition.append(footPosition.FootPosition(Legs.sideLengthOfHex, thisCoxaRotation, Legs.coxaLength, Legs.femurLength, Legs.tibiaLength, Legs.stanceFemurAngle, Legs.stanceTibiaAngle))

    def footPositions(self):
        return Legs.footPosition

    def setOneLeg(self, leg, servoCoxaAngle, servoFemurAngle, servoTibiaAngle):
        """Sets indicated legs to a given set of angles"""
        self._servos.setServo(self.legServoPins[leg][0], self.servoLookupCoxa[(servoCoxaAngle-self.neutral[leg][0])%360])
        self._servos.setServo(self.legServoPins[leg][1], self.servoLookupFemur[(servoFemurAngle-self.neutral[leg][1])%360])
        self._servos.setServo(self.legServoPins[leg][2], self.servoLookupTibia[(servoTibiaAngle-self.neutral[leg][2])%360])

    def setAllLegsToSamePosition(self, servoCoxaAngle, servoFemurAngle, servoTibiaAngle):
        """Sets all legs to a given set of angles"""
        for leg in range(0, 6):
            self.setOneLeg(leg, servoCoxaAngle, servoFemurAngle, servoTibiaAngle)

    def setAllLegs(self, allLegPositions):
        """Sets each legs to its position given set of positions"""
        i = 0
        for leg in allLegPositions:
            self.setOneLeg(i, leg[0], leg[1], leg[2])
            i = i+1

    def setInitialStance(self):
        """Sets all legs to the pre-defined initial stance angles"""
        self.setAllLegsToSamePosition(self.stanceCoxaAngle, self.stanceFemurAngle, self.stanceTibiaAngle)

    def settleToInitialStance(self, leg):
        """Move a leg to its initial stance angles"""
        self._servos.setServo(self.legServoPins[leg][1], self.servoLookupFemur[(self.stanceFemurAngle+30-self.neutral[leg][1])%360])
        self._servos.setServo(self.legServoPins[leg][2], self.servoLookupTibia[(self.stanceTibiaAngle-self.neutral[leg][2])%360])
        time.sleep(.2)
        self._servos.setServo(self.legServoPins[leg][0], self.servoLookupCoxa[(self.stanceCoxaAngle-self.neutral[leg][0])%360])
        time.sleep(.2)
        self._servos.setServo(self.legServoPins[leg][1], self.servoLookupFemur[(self.stanceFemurAngle-self.neutral[leg][1])%360])
        time.sleep(.2)

class TestLegs(unittest.TestCase):

    def setUp(self):
        self.legs = Legs()

    def test_legs_setup(self):
        self.legs.setInitialStance()
        time.sleep(1)
        self.legs.setOneLeg(4,90,50,50)
        time.sleep(2)
        self.legs._servos.end()

        
if __name__ == '__main__':
    unittest.main()
