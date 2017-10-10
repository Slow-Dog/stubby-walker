import cProfile, pstats, StringIO
import time
import cwiid
import servos
import animation
import breathe
##import datetime as dt

print "Initialising"

##Gait Setup
legLiftHeight = 20
travelLength = 30
travelRotation = 10

travelLength2 = travelLength*2
travelLength4 = travelLength*4

##Animation is initialised with step and rotion distances
ani = animation.Animation(travelLength, travelRotation, legLiftHeight)

def wiiloop():
    print 'Press button 1 + 2 on your Wii Remote...'
    time.sleep(1)

    #Try Wii Remote until connected
    Wii = None
    i = 1
    while not Wii:
        try:
            Wii = cwiid.Wiimote()
        except RuntimeError:
            if i > 100:
                quit()
                break
            print "Error opening wiimote connection"
            print "attempt " + str(i)
            i += 1
    
    print 'Wii Remote connected...'
    print '\nPress the HOME button to disconnect the Wii and end the application'
    time.sleep(1)
    
    Wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
    
    Counter = 0
    
    Wii.rumble = True
    time.sleep(0.25)
    Wii.rumble = False

    if Wii:
        loop = True
        while loop:
            xDistanceStepped = 0
            yDistanceStepped = 0
            zDistanceStepped = 0
            xAngleStepped = 0
            yAngleStepped = 0
            zAngleStepped = 0
            buttons = Wii.state['buttons']
#            if buttons ! = 0:
#            print 'State: ', buttons
    
            if buttons & cwiid.BTN_A:
                tilt = Wii.state['acc']
                if tilt[0] <= 120:
                    xAngleStepped = -1
                if tilt[0] >= 136:
                    xAngleStepped = 1
                if tilt[1] <= 120:
                    yAngleStepped = -1
                if tilt[1] >= 136:
                    yAngleStepped = 1

            ##If holding trigger step left and right, else turn left and right
            if buttons & cwiid.BTN_B:
                if buttons & cwiid.BTN_LEFT:
                    xDistanceStepped = -2
                if buttons & cwiid.BTN_RIGHT:
                    xDistanceStepped = 2
            else:
                if buttons & cwiid.BTN_LEFT:
                    zAngleStepped = -1
                if buttons & cwiid.BTN_RIGHT:
                    zAngleStepped = 1
            if buttons & cwiid.BTN_UP:
                yDistanceStepped = 2
            if buttons & cwiid.BTN_DOWN:
                yDistanceStepped = -2
            if buttons & cwiid.BTN_PLUS:
                zDistanceStepped = 1
            if buttons & cwiid.BTN_MINUS:
                zDistanceStepped = -1

            if buttons & cwiid.BTN_HOME:
    #                print 'closing Bluetooth connection. Good Bye!'
    ##                tap(2)
    #            exit()
                loop = False
            if (xDistanceStepped == 0 and yDistanceStepped == 0 and zDistanceStepped == 0 
            and xAngleStepped == 0 and yAngleStepped == 0 and zAngleStepped == 0):
                servos.stop()
            else:
                ani.step(xDistanceStepped, yDistanceStepped, zDistanceStepped, xAngleStepped, yAngleStepped, zAngleStepped)

servos = servos.Servos()

print "Initialised"

time.sleep(1)

#Centre
ani.setInitialStance()

time.sleep(1)

servos.stop()
         
wiiloop()

ani.settleToInitialStance()

#pr = cProfile.Profile()
#pr.enable()

###b = breathe.breathe(10, 1000)
###b.start()

#for i in range(10000):
#    ani.step(1, 0, 0, 0, 0, 0)

###b.stop();

#pr.disable()
#s = StringIO.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream = s).sort_stats(sortby)
#ps.print_stats()
#print s.getvalue()

#time.sleep(1)
#legs.setAllLegs(0, 0, 0)
#time.sleep(1)

servos.end()
