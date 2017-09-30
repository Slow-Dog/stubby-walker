import time
import math
import cwiid
import servos
import legs
import mathLookup
import vectorMath
import stepMath
import breathe
import cProfile, pstats, StringIO
##import datetime as dt

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
legs = legs.Legs()

leg = []

leg = legs.footPositions()

##Gait Setup
legLiftHeight = 20
travelLength = 30
travelRotation = 15

travelLength2=travelLength*2
travelLength4=travelLength*4

##StepMath iterates leg positions over step distances, converting a moving position into a walk
sm = stepMath.StepMath(travelLength, travelRotation, legLiftHeight)

servos = servos.Servos()

print "Initialised"

time.sleep(1)

#Centre
legs.setInitialStance()

legAngles = [0] * 6

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

def walk(steps):
  #IKRaise
  bodyRotation=[0,0,0]
  bodyPosition=[0,0,0]

  bodyRotationAdd=[0,0,0] 
  bodyPositionAdd=[0,2,0]

  for k in [1]:

  ##  n1=dt.datetime.now()
    for j in range(0, steps):
  ##    legAngles = calculateLegAngles (vAddTotal, vRotateTotal)
  ##    print legAngles
  ##    print


  #    #calculate relative angles to that position
  #    #Step x, y and rotation around z-axis
  #    bodyPositionForLeft, bodyRotationForLeft, bodyPositionForRight, bodyRotationForRight = sm.relativeBodyPositionsFromStep(bodyPositionAdd[0],bodyPositionAdd[1],bodyRotationAdd[2])

  #    ##relativeBodyPositionsFromStep only calculates x distance, y distance, and rotation around z-axis as those are used for walking.
  #    ##Rotation around x and y, and z-axis distance, can be used for posing while walking.
  #    ##Add in torso rotation, height here, eventually

  #    #left Leg
  #    for i in range(0, 6, 2):
  #      legAngles[i] = leg[i].calcIKFootPosition(bodyPositionForLeft, bodyRotationForLeft)
  #    #right Leg
  #    for i in range(1, 6, 2):
  #      legAngles[i] = leg[i].calcIKFootPosition(bodyPositionForRight, bodyRotationForRight)
  ###      print legAngles[i]
      
      #calculate relative angles to that position
      #Step x, y and rotation around z-axis
      bodyPosition, bodyRotation = sm.allRelativeBodyPositionsFromStep(bodyPositionAdd[0],bodyPositionAdd[1],bodyRotationAdd[2])

      ##relativeBodyPositionsFromStep only calculates x distance, y distance, and rotation around z-axis as those are used for walking.
      ##Rotation around x and y, and z-axis distance, can be used for posing while walking.
      ##Add in torso rotation, height here, eventually


      for i in range(0, 6):
        #set servos to that position
        legAngles[i] = leg[i].calcIKFootPosition(bodyPosition[i], bodyRotation[i])
        legs.setOneLeg(i, legAngles[i][0], legAngles[i][1], legAngles[i][2])
      
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



##pr = cProfile.Profile()
##pr.enable()

#b = breathe.breathe(10, 1000)
#b.start()

walk(1000)

#b.stop();

##pr.disable()
##s = StringIO.StringIO()
##sortby = 'cumulative'
##ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
##ps.print_stats()
##print s.getvalue()
##
##walk()

time.sleep(1)
#legs.setAllLegs(0, 0, 0)
#time.sleep(1)

servos.end()
