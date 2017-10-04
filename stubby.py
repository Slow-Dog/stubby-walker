import time
import math
import cwiid
import servos
import legs
import stepMath
import breathe
import cProfile, pstats, StringIO
##import datetime as dt

print "Initialising"

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

def waswalk(steps):
  #IKRaise
  bodyRotation=[0,0,0]
  bodyPosition=[0,0,0]

  bodyRotationAdd=[0,0,0] 
  bodyPositionAdd=[0,2,0]

  for k in [1]:

  ##  n1=dt.datetime.now()
    for j in range(0, steps):
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

    n2=dt.datetime.now()
    print ((n2-n1).microseconds)/1e6

def walk(x, y, z):
  #print x, y, z
  #IKRaise
  bodyRotation=[0,0,0]
  bodyPosition=[0,0,0]

  #Step x, y and rotation around z-axis
  bodyPosition, bodyRotation = sm.allRelativeBodyPositionsFromStep(x,y,z)

  ##relativeBodyPositionsFromStep only calculates x distance, y distance, and rotation around z-axis as those are used for walking.
  ##Rotation around x and y, and z-axis distance, can be used for posing while walking.
  ##Add in torso rotation, height here, eventually

  for i in range(0, 6):
    #set servos to that position
    legAngles[i] = leg[i].calcIKFootPosition(bodyPosition[i], bodyRotation[i])
    legs.setOneLeg(i, legAngles[i][0], legAngles[i][1], legAngles[i][2])
      
  #    time.sleep (.2)

print 'Press button 1 + 2 on your Wii Remote...'
time.sleep(1)
  
#Try Wii Remote until connected
Wii = None 
i=1 
while not Wii: 
  try: 
    Wii=cwiid.Wiimote() 
  except RuntimeError: 
    if (i>100): 
      quit() 
      break 
    print "Error opening wiimote connection" 
    print "attempt " + str(i) 
    i +=1 
  
print 'Wii Remote connected...'
print '\nPress the PLUS button to disconnect the Wii and end the application'
time.sleep(1)
  
Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
  
Counter = 0
  
Wii.rumble=True
time.sleep(0.25)
Wii.rumble = False
  
if Wii:
  wiiloop = True
  while wiiloop:
    x=0
    y=0
    z=0
    buttons=Wii.state['buttons']
##    if buttons != 0:
##      print 'State: ', buttons
  
    if buttons & cwiid.BTN_A:
      tilt = Wii.state['acc']
      if tilt[0] <= 120:
        print "Tilt Left"
      if tilt[0] >= 136:
        print "Tilt Right"
      if tilt[1] <= 120:
        print "Tilt Back"
      if tilt[1] >= 136:
        print "Tilt Fwd"

    ##If holding trigger step left and right, else turn left and right
    if buttons & cwiid.BTN_B:
      if buttons & cwiid.BTN_LEFT:
        x=-2
      if buttons & cwiid.BTN_RIGHT:
        x=2
    else:
      if buttons & cwiid.BTN_LEFT:
        z=-1
      if buttons & cwiid.BTN_RIGHT:
        z=1
    if buttons & cwiid.BTN_UP:
      y=2
    if buttons & cwiid.BTN_DOWN:
      y=-2
    if buttons & cwiid.BTN_HOME:
#        print 'closing Bluetooth connection. Good Bye!'
##        tap(2)
      exit(Wii)
      wiiloop = False
    if (x==0 and y==0 and z==0):
      servos.stop()
    else:
      walk (x, y, z)


#pr = cProfile.Profile()
#pr.enable()

##b = breathe.breathe(10, 1000)
##b.start()

###walk(10000)

##b.stop();

#pr.disable()
#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#ps.print_stats()
#print s.getvalue()
###
###walk()

#time.sleep(1)
#legs.setAllLegs(0, 0, 0)
#time.sleep(1)

servos.end()
