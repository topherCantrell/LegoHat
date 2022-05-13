import threading

import motors
import display

import RPi.GPIO as GPIO

high_activity = [True]

def btpress(channel):
    global disp, mot_top, mot_front,mot_side
    high_activity[0] = not high_activity[0]    

disp = threading.Thread(target=display.main_loop,args=(high_activity,))
disp.start()
mot_top = threading.Thread(target=motors.main_loop,args=(high_activity,2))
mot_top.start()
mot_front = threading.Thread(target=motors.main_loop,args=(high_activity,0))
mot_front.start()
mot_side = threading.Thread(target=motors.main_loop,args=(high_activity,1))
mot_side.start()

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(21,GPIO.FALLING, callback=btpress,bouncetime=300)


