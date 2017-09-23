import time
import math
import cwiid
import pigpio
import mathLookup
import vectorMath
import legMath
import stepMath
import breathe
import cProfile, pstats, StringIO
##import datetime as dt

##Set a servo to a poistion in degrees
def setServoDegrees ( servoNum, position ):
    ##Calls pigpio to set a servo to a position. 0 degrees is centred, so range is usually -90 to +90
#      print ("Servo {} {} micro pulses".format(s, pw))
  pw = int (round(position * 500.0 / 90.0 + 1500))
  if (pw>=500 and pw <=2500) :
    pigs.set_servo_pulsewidth(servoNum, pw)

def setServo ( servoNum, pw ):
##  print "Servo ", servoNum, " set to ", pw 
  if (pw>=500 and pw <=2500) :
    pigs.set_servo_pulsewidth(servoNum, pw)

def setAllLegs (servoCoxaAngle, servoFemurAngle, servoTibiaAngle):
  for leg in range (0, 6):
    setOneLeg (leg, servoCoxaAngle, servoFemurAngle, servoTibiaAngle)

def setOneLeg (leg, servoCoxaAngle, servoFemurAngle, servoTibiaAngle):
##  print "Coxa ", servoCoxaAngle, " Femur ", servoFemurAngle, " Tibia ", servoTibiaAngle 
  setServo ( legs[leg][0], servoLookupCoxa[servoCoxaAngle%360]-neutral[leg][0])
  setServo ( legs[leg][1], servoLookupFemur[servoFemurAngle%360]-neutral[leg][1])
  setServo ( legs[leg][2], servoLookupTibia[servoTibiaAngle%360]-neutral[leg][2])

def calculateLegAngles (vecOffset, vecRotate):
  legAngles = [0] * 6
  for i in range(0, 6):
    ##Body Forward Kinematics
    ##Rotate and translate initial Coxa Positions to desired current body position
    
    #Each axis rotation
    newCoxaPosition = v.rotate(initialCoxaPosition[i], vecRotate[0], vecRotate[1], vecRotate[2])

    #add current body translation
    newCoxaPosition = v.add3dVector(newCoxaPosition, vecOffset)
    
    ##Calculate the Leg angles required to point the leg from the new body position to their inital position
    legAngles[i] = lmath.calcLegAngles(newCoxaPosition, initialFootPosition[i])
  return legAngles

print "Initialising"

m = mathLookup.MathLookup()
v = vectorMath.VectorMath()

#servo pin numbers
servos = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

#servo pin numbers for each leg [coxa, femur, tibia] joints
legs = [[2, 8, 9], [12, 4, 17], [5 ,14, 3] , [7,16, 19] , [18,13,6] , [15,10, 11]]

#neutral offset. Angle to add when set to 0 to get joint to zero
#found by programmatically setting the robot leg positions to zero and measuring
neutral = [[-3,0,0],[-0,-0, 0],[-5,0,0],[9,0,0],[13,-0,0],[0,0,0]]

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
##  Coxa     Femur    
##    |      |    
##    V      V    
##  _ _ __ _ _    
## /   |__|   \ <- Tibia
##     
##     


sideLengthOfHex = 47
coxaLength = 53
femurLength= 40
tibiaLength = 58

coxaRotationDirection=1

## For a simple joint the leg is connected to the servo and rotates the joint directly.
## Set complx<joint> to False
## 
## A complex joint uses a pushrod connected to a servo horn to move the joint indirectly
## This is labelling:
##
##           Clength
##          *------.---0  
## Dlength |      /   
##        |      / Blength (Pushrod)   
##      [O]-----o          
##       Alength (Servo horn)         
##              
## Note all lengths are measured between pivot points and joints.
## Thus the Femur Length is from the Femur joint to Tibia Joint,
## while the FemurCLength is from the Femur joint to where the pushrod is connected to the femur

complexFemur = True
femurAlength=15
femurBlength=55
femurClength=35
femurDlength=26

## The basic calculations assume the angle * in the above diagram is 90 degrees
## i.e. that the joint is above the servo.
## If it isn't, then the offset angle is the amount more that 90 degrees
femurOffsetAngle=35

## If your servo is mounted the opposite way to mine,
## and the joint contracts when it should expand,
## set this to -1
## Valid for simple and complex joints
femurRotationDirection=1

## Same again for Tibia
complexTibia = True
tibiaAlength=17
tibiaBlength=41
tibiaClength=35
tibiaDlength=29
tibiaOffsetAngle=25
tibiaRotationDirection=1

## And again for Coxa
complexCoxa = False
coxaAlength=0
coxaBlength=0
coxaClength=0
coxaDlength=0
coxaOffsetAngle=0
coxaRotationDirection=1

#Define initial stance
#Use internal angles, where 0 = folded, 180 is open
femurAngle = 70
tibiaAngle = 90

#height of femur joint over robot centre
femurJointHeight = 35.0

## Use the above values to form lookup tables.
## The live calculations determine leg joint angles,
## and these lookups calculate servo settings for the joint angle.
servoLookupCoxa = []
servoLookupFemur = []
servoLookupTibia = []
for a in range (0,360):
  servoLookupCoxa.append (int ((a-90)/90.0*1000.0*coxaRotationDirection)+1500)
  
  if (complexFemur):
    e1 = m.mathCosineRuleLength(femurClength, femurDlength, a+femurOffsetAngle)
    if (e1 < femurBlength+femurAlength) and (e1 > femurBlength-femurAlength):
      a1 = m.mathCosineRuleAngle(e1, femurDlength, femurClength)
      a2 = m.mathCosineRuleAngle(e1, femurAlength, femurBlength )
      servoLookupFemur.append (int ((a1+a2-90)/90*1000*femurRotationDirection)+1500)
    else:
      a1=0
      a2=0
      servoLookupFemur.append (0)
  else:
    servoLookupFemur.append (int ((a-90)/90.0*1000.0*femurRotationDirection)+1500)
      
  if (complexTibia):
    e2 = m.mathCosineRuleLength(tibiaClength, tibiaDlength, a+tibiaOffsetAngle)
    if (e2 < tibiaBlength+tibiaAlength) and (e1 > tibiaBlength-tibiaAlength):
      a3 = m.mathCosineRuleAngle(e2, tibiaDlength, tibiaClength)
      a4 = m.mathCosineRuleAngle(e2, tibiaAlength, tibiaBlength )
      servoLookupTibia.append (int ((a3+a4-90)/90*1000*tibiaRotationDirection)+1500)
    else:
      a3=0
      a4=0
      servoLookupTibia.append (0)
  else:
    servoLookupTibia.append (int ((a-90)/90.0*1000.0*tibiaRotationDirection)+1500)
##for a in range (0, 190, 10):
##  print a, ",",servoLookupFemur[a], ",",servoLookupTibia[a], ",",
##  print a, ",",servoLookupCoxa[a]
##  print


#Store initial coxa and foot positions, used when calculating dynamic joint angles
##initialCoxaRotation = [0] * 6
##initialCoxaPosition = [0.0] * 6
##initialFootPosition = [0.0] * 6
##
##initialLegLengthX =  0
##initialLegLengthY =  int(sideLengthOfHex + coxaLength + femurLength * m.sin(femurAngle) - tibiaLength * m.cos(femurAngle+tibiaAngle-90))
##initialLegLengthZ =  int(femurLength * m.cos(femurAngle) + tibiaLength * m.sin(femurAngle+tibiaAngle-90))

leg = []

##rotate around to define each initial position of each coxa and foot
##If your Hexapod isn't rotationally symmetrical, set them manually
for i in range(0,6):
  thisCoxaRotation = i*60-30
  leg.append (legMath.LegMath(sideLengthOfHex, thisCoxaRotation, coxaLength, femurLength, tibiaLength, femurAngle, tibiaAngle))

##Gait Setup
legLiftHeight = 20
travelLength = 30
travelRotation = 15

travelLength2=travelLength*2
travelLength4=travelLength*4

##StepMath iterates leg positions over step distances, converting a moving position into a walk
sm = stepMath.StepMath(travelLength, travelRotation, legLiftHeight)

pigs = pigpio.pi() # Initialise pigpio functions, used for controlling servos

print "Initialised"

time.sleep(1)

#Centre
legAngles = [0] * 6
setAllLegs(90, femurAngle, tibiaAngle)

  ##for a in [60, 70, 80, 90, 100, 110, 120, 130, 140]:
  ##  print a
  ##  setAllLegs(90, femurAngle, a)
  ##  time.sleep (.1)
   
  ##for a in [0, -10, -20, -30, 0]:
  ###  print rotate ([100,0,0], 0, 0, a)
  ##  legAngles = calculateLegAngles ([0,0,0], [0,0,a])
  ###  print a, legAngles[0]
  ###  print
  ##  #set servos to that position
  ##  for i in range(0, 6):
  ##    setOneLeg(i, legAngles[i][0], legAngles[i][1], legAngles[i][2])
  ###setAllLegs(90, femurAngle, tibiaAngle)
  ##  time.sleep(2)

def walk():
  #IKRaise
  bodyRotation=[0,0,0]
  bodyPosition=[0,0,0]

  bodyRotationAdd=[0,0,0] 
  bodyPositionAdd=[1,0,0]

  for k in [1]:

  ##  n1=dt.datetime.now()
    for j in range(0, 10000):
  ##    legAngles = calculateLegAngles (vAddTotal, vRotateTotal)
  ##    print legAngles
  ##    print


      #calculate relative angles to that position
      #Step x, y and rotation around z-axis
      bodyPositionForLeft, bodyRotationForLeft, bodyPositionForRight, bodyRotationForRight = sm.relativeBodyPositionsFromStep(bodyPositionAdd[0],bodyPositionAdd[1],bodyRotationAdd[2])

      ##relativeBodyPositionsFromStep only calculates x distance, y distance, and rotation around z-axis as those are used for walking.
      ##Rotation around x and y, and z-axis distance, can be used for posing while walking.
      ##Add in torso rotation, height here, eventually

      #left Leg
      for i in range(0, 6, 2):
        legAngles[i] = leg[i].calcIKFootPosition(bodyPositionForLeft, bodyRotationForLeft)
      #right Leg
      for i in range(1, 6, 2):
        legAngles[i] = leg[i].calcIKFootPosition(bodyPositionForRight, bodyRotationForRight)
  ##      print legAngles[i]
      
      for i in range(0, 6):
        #set servos to that position
        setOneLeg(i, legAngles[i][0], legAngles[i][1], legAngles[i][2])
      
  #    time.sleep (.2)

  ##  n2=dt.datetime.now()
  ##  print ((n2-n1).microseconds)/1e6


  ##print 'Press button 1 + 2 on your Wii Remote...'
  ##time.sleep(1)
  ##
  ###Try Wii Remote until connected
  ##Wii = None 
  ##i=1 
  ##while not Wii: 
  ##  try: 
  ##    Wii=cwiid.Wiimote() 
  ##  except RuntimeError: 
  ##    if (i>100): 
  ##      quit() 
  ##      break 
  ##    print "Error opening wiimote connection" 
  ##    print "attempt " + str(i) 
  ##    i +=1 
  ##
  ##print 'Wii Remote connected...'
  ##print '\nPress the PLUS button to disconnect the Wii and end the application'
  ##time.sleep(1)
  ##
  ##Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
  ##
  ##Counter = 0
  ##
  ##Wii.rumble=True
  ##time.sleep(0.25)
  ##Wii.rumble = False
  ##
  ##if Wii:
  ##  while True:
  ##    buttons=Wii.state['buttons']
  ##    if buttons != 0:
  ##        print 'State: ', buttons
  ##
  ##    if buttons & cwiid.BTN_A:
  ##      tilt = Wii.state['acc']
  ##      if tilt[0] <= 120:
  ##        print "Tilt Left"
  ##      if tilt[0] >= 136:
  ##        print "Tilt Right"
  ##      if tilt[1] <= 120:
  ##        print "Tilt Back"
  ##      if tilt[1] >= 136:
  ##        print "Tilt Fwd"

  #if (buttons & cwiid.BTN_DOWN):
  ##    if b == 1024:
  ##        walkFwd(1)
  ## 
  ##    if b == 2048:
  ##        walkBwd(1)
  ## 
  ##    if b == 256:
  ##        spinLeftN(1)
  ## 
  ##    if b == 512:
  ##        spinRightN(1)
  ##
  ##    if b == 1280:
  ##        turnLeft()
  ## 
  ##    if b == 1536:
  ##        turnRight()

  ##    if buttons == 4096:
  ###        print 'closing Bluetooth connection. Good Bye!'
  ##        tap(2)
  ##        exit(Wii)



pr = cProfile.Profile()
pr.enable()

#b = breathe.breathe(10, 1000)
#b.start()

walk()

#b.stop();

pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()

##walk()

#setAllLegs(0, 0, 0)
#time.sleep(1)

##for s in servos:
##   pigs.set_servo_pulsewidth(s, 1500);

# switch all servos off
for s in servos:
   pigs.set_servo_pulsewidth(s, 0);

pigs.stop()
