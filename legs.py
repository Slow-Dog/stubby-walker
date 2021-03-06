from array import *
import copy
import unittest
import mathLookup
import footPosition
import servos
import time

class Legs:

    #servo pin numbers for each leg [coxa, femur, tibia] joints
    legServoPins = [[12, 8, 9], [5, 4, 17], [7, 14, 3], [18, 16, 19], [15, 13, 6], [2, 10, 11]]

    _lastPosition = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    init = False

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
    ##      ^   Alength (Servo horn)                
    ##      |
    ##      Servo
    ##
    ## Note all lengths are measured between pivot points and joints.
    ## Thus the Femur Length is from the Femur joint to Tibia Joint,
    ## while the FemurCLength is from the Femur joint to where the pushrod is connected to the femur

    complexFemur = True
    femurAlength = 15
    femurBlength = 41
    femurClength = 35
    femurDlength = 26

    ## The basic calculations assume the angle * in the above diagram is 90 degrees
    ## i.e. that the joint is above the servo.
    ## If it isn't, then the offset angle is the amount more that 90 degrees
    femurOffsetAngle = 35

    ## The calculations assume the servo's middle position is at 90 degrees to leg D
    ## If it isn't, adjust the following angle
    femurServoMiddlePosition = 90

    ## If your servo is mounted the opposite way to mine,
    ## and the joint contracts when it should expand,
    ## set this to -1
    ## Valid for simple and complex joints
    femurRotationDirection = 1

    ## Same again for Tibia
    complexTibia = True
    tibiaAlength = 17
    tibiaBlength = 55
    tibiaClength = 35
    tibiaDlength = 29
    tibiaOffsetAngle = 25
    tibiaRotationDirection = 1
    tibiaServoMiddlePosition = 90

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
    stanceFemurAngle = 80
    stanceTibiaAngle = 75

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
        if not self.init:
            self.init = True
            for a in range(0, 360):
                #pw1 = int((a-90)/90.0*1000.0*Legs.coxaRotationDirection)+1500
                #pw1 = int((a+90)*Legs.coxaRotationDirection)
                pw1 = int((a)*Legs.coxaRotationDirection)
                Legs.servoLookupCoxa.append(pw1)
                if Legs.complexFemur:
                    e1 = Legs._mathLookup.mathCosineRuleLength(Legs.femurClength, Legs.femurDlength, a+Legs.femurOffsetAngle)
                    if (e1 < Legs.femurBlength+Legs.femurAlength) and (e1 > Legs.femurBlength-Legs.femurAlength):
                        a1 = Legs._mathLookup.mathCosineRuleAngle(e1, Legs.femurDlength, Legs.femurClength)
                        a2 = Legs._mathLookup.mathCosineRuleAngle(e1, Legs.femurAlength, Legs.femurBlength)
                        #Legs.servoLookupFemur.append(int((a1+a2-90)/90*1000*Legs.femurRotationDirection)+1500)
                        Legs.servoLookupFemur.append(int(((a1+a2-self.femurRotationDirection)*Legs.femurRotationDirection)%360))
                    else:
                        a1 = 0
                        a2 = 0
                        Legs.servoLookupFemur.append(0)
                    #print a, Legs.servoLookupFemur[a]
                else:
                    Legs.servoLookupFemur.append(int((a-90)/90.0*1000.0*Legs.femurRotationDirection)+1500)

                if Legs.complexTibia:
                    e2 = Legs._mathLookup.mathCosineRuleLength(Legs.tibiaClength, Legs.tibiaDlength, a+Legs.tibiaOffsetAngle)
                    if (e2 < Legs.tibiaBlength+Legs.tibiaAlength) and (e1 > Legs.tibiaBlength-Legs.tibiaAlength):
                        a3 = Legs._mathLookup.mathCosineRuleAngle(e2, Legs.tibiaDlength, Legs.tibiaClength)
                        a4 = Legs._mathLookup.mathCosineRuleAngle(e2, Legs.tibiaAlength, Legs.tibiaBlength)
                        #Legs.servoLookupTibia.append(int((a3+a4-90)/90*1000*Legs.tibiaRotationDirection)+1500)
                        Legs.servoLookupTibia.append(int(((a3+a4-self.tibiaServoMiddlePosition)*Legs.tibiaRotationDirection)%360))
                    else:
                        a3 = 0
                        a4 = 0
                        Legs.servoLookupTibia.append(0)
                else:
                    Legs.servoLookupTibia.append(int((a-90)/90.0*1000.0*Legs.tibiaRotationDirection)+1500)

            ##rotate around to define each initial position of each foot for a coxa angle
            ##If your Hexapod isn't rotationally symmetrical, set them manually
            for i in range(0, 6):
                thisCoxaRotation = i*60-30
                Legs.footPosition.append(footPosition.FootPosition(Legs.sideLengthOfHex, thisCoxaRotation, Legs.coxaLength, Legs.femurLength, Legs.tibiaLength, Legs.stanceFemurAngle, Legs.stanceTibiaAngle))

    def footPositions(self):
        return Legs.footPosition

    def getLegAngles(self):
        return copy.deepcopy(self._lastPosition)

    def getOneLegAnglesFromServoAngles(self, leg, servoCoxaAngle, servoFemurAngle, servoTibiaAngle):
        nearestServoCoxaAngle=360
        diff=360
        for a in self.servoLookupCoxa:
            if abs(servoCoxaAngle-a) < diff:
                diff = abs(servoCoxaAngle-a)
                nearestServoCoxaAngle = a
        nearestServoFemurAngle=360
        diff=360
        for a in self.servoLookupFemur:
            if abs(servoFemurAngle-a) < diff:
                diff = abs(servoFemurAngle-a)
                nearestServoFemurAngle = a
        nearestServoTibiaAngle=360
        diff=360
        for a in self.servoLookupTibia:
            if abs(servoTibiaAngle-a) < diff:
                diff = abs(servoTibiaAngle-a)
                nearestServoTibiaAngle = a
        return self.servoLookupCoxa.index(nearestServoCoxaAngle), self.servoLookupFemur.index(nearestServoFemurAngle), self.servoLookupTibia.index(nearestServoTibiaAngle)

    def setOneLeg(self, leg, coxaAngle, femurAngle, tibiaAngle):
        """Sets indicated legs to a given set of angles"""
        self.setOneLegServoAngles(leg,
                                  self.servoLookupCoxa[(int(coxaAngle))%360],
                                  self.servoLookupFemur[(int(femurAngle))%360],
                                  self.servoLookupTibia[(int(tibiaAngle))%360])
        self._lastPosition[leg][0] = coxaAngle
        self._lastPosition[leg][1] = femurAngle
        self._lastPosition[leg][2] = tibiaAngle

    def setOneLegServoAngles(self, leg, coxaAngle, femurAngle, tibiaAngle):
        self._servos.setServoDegrees(self.legServoPins[leg][0], coxaAngle)
        self._servos.setServoDegrees(self.legServoPins[leg][1], femurAngle)
        self._servos.setServoDegrees(self.legServoPins[leg][2], tibiaAngle)

    def setAllLegsToSamePosition(self, coxaAngle, femurAngle, tibiaAngle):
        """Sets all legs to a given set of angles"""
        for leg in range(0, 6):
            self.setOneLeg(leg, coxaAngle, femurAngle, tibiaAngle)

    def initialiseLastPosition(self, coxaAngle, femurAngle, tibiaAngle):
        for leg in range(0, 6):
            self._lastPosition[leg][0] = coxaAngle
            self._lastPosition[leg][1] = femurAngle
            self._lastPosition[leg][2] = tibiaAngle

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
        self._servos.setServoDegrees(self.legServoPins[leg][1], self.servoLookupFemur[(self.stanceFemurAngle+30)%360])
        self._servos.setServoDegrees(self.legServoPins[leg][2], self.servoLookupTibia[(self.stanceTibiaAngle)%360])
        time.sleep(.2)
        self._servos.setServoDegrees(self.legServoPins[leg][0], self.servoLookupCoxa[(self.stanceCoxaAngle)%360])
        time.sleep(.2)
        self._servos.setServoDegrees(self.legServoPins[leg][1], self.servoLookupFemur[(self.stanceFemurAngle)%360])
        time.sleep(.2)

class TestLegs(unittest.TestCase):

    def setUp(self):
        self.legs = Legs()

    def test_legs_setup(self):
        self.legs.setInitialStance()
        time.sleep(3)
##        self.legs.setOneLeg(0, 0, 80, 110)
##        time.sleep(1)
        
##        self.legs.settleToInitialStance(0)
##        self.legs.settleToInitialStance(3)
##        self.legs.settleToInitialStance(1)
##        self.legs.settleToInitialStance(4)
##        self.legs.settleToInitialStance(2)
##        self.legs.settleToInitialStance(5)
##        time.sleep(1)
        time.sleep(1)
        self.legs._servos.stop()

    def test_getOneLegAnglesFromServoAngles(self):
        #print self.legs.getOneLegAnglesFromServoAngles(0, 90, 90, 90)
#        self.legs.setOneLeg(0, 0, 107, 105)
        #print self.legs.getLegAngles()
        print

       
if __name__ == '__main__':
    unittest.main()
