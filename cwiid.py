import time
import threading

RPT_ACC = 0
RPT_BTN = 0

BTN_A = 1
BTN_B = 2
BTN_LEFT = 4
BTN_RIGHT = 8
BTN_UP = 16
BTN_DOWN = 32
BTN_PLUS = 64
BTN_MINUS = 128
BTN_HOME = 256

class Wiimote:

  rumble = False
  rpt_mode = 0
  tilt = [0, 0]
  state = {'buttons': 0, 'acc': tilt}

  def __init__(self):
    threading.Thread(target=self.pressButtons).start()
    self.i=0

  def pressButtons(self):
    buttonPresses = [BTN_A | BTN_MINUS, BTN_A | BTN_MINUS]
    for b in buttonPresses:
      self.state['buttons'] = b
      time.sleep(10)
    self.state['buttons'] = BTN_HOME
