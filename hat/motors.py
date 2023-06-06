import board
import adafruit_motorkit

import time
import random

kit = adafruit_motorkit.MotorKit()

MOTORS = [ #      -FAST  -MED   -SLOW  STOP  +SLOW +MED  +FAST
    (kit.motor1, [-1.00, -0.75, -0.50, None, 0.50, 0.75, 1.00]),
    (kit.motor2, [-1.00, -0.90, -0.80, None, 0.80, 0.90, 1.00]),
    (kit.motor3, [-0.95, -0.85, -0.75, None, 0.75, 0.85, 0.95]),
]

runs = [
    [(4,10),(3,5),(2,20),(1,30),(3,10),(5,20)], # 9.5s total
    [(4,10),(6,30)], # 4s total
    [(2,10),(0,30)], # 4s total
    [(4,10),(3,5),(2,10),(3,5),(4,10),(3,5),(2,10)], # 5.5s total
    [(6,30)], # 3s total
    [(0,30)], # 3s total
]

def main_loop(sleep_mode, motor_number):
    motor, speeds = MOTORS[motor_number]
    while True:
        _loop(sleep_mode, motor, speeds)
        motor.throttle = None
        while sleep_mode[0]:
            time.sleep(0.25)
        

def _loop(sleep_mode, motor, speeds):        
    while True:
        # Abort if the sleep-switch was pressed
        if sleep_mode[0]:
            return
        # Pick an activity profile
        run = random.choice(runs)
        for v,delay in run:
            thr = speeds[v]            
            motor.throttle = thr
            for _ in range(delay):
                if sleep_mode[0]:
                    return
                time.sleep(0.1)
        motor.throttle = None
        # Pause for a few seconds between runs
        for _ in range(random.choice([10,15,18,20])):
            if sleep_mode[0]:
                return
            time.sleep(0.1)

if __name__ == '__main__':
    main_loop(2)