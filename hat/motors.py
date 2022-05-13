import board
import adafruit_motorkit

import time
import random

kit = adafruit_motorkit.MotorKit()

MOTORS = [
    (kit.motor1,[-1.0,-0.75,-0.50,None,0.50,0.75,1]),
    (kit.motor2,[-1.0,-0.90,-0.80,None,0.80,0.90,1]),
    (kit.motor3,[-0.95,-0.85,-0.75,None,0.75,0.85,0.95]),
]

runs = [
    [(4,10),(3,5),(2,20),(1,30),(3,10),(5,20)], # 9.5s
    [(4,10),(6,30)], # 4s
    [(2,10),(0,30)], # 4s
    [(4,10),(3,5),(2,10),(3,5),(4,10),(3,5),(2,10)], # 5.5s
    [(6,30)], # 3s
    [(0,30)], # 3s
]

def main_loop(high_activity,motor_number):
    mot,vals = MOTORS[motor_number]
    while True:
        _loop(high_activity,mot,vals)
        mot.throttle = None
        while not high_activity[0]:
            time.sleep(0.25)
        

def _loop(high_activity,mot,vals):        
    while True:
        if not high_activity[0]:
            return
        run = random.choice(runs)
        for v,delay in run:
            thr = vals[v]
            #print(thr,delay)
            mot.throttle = thr
            for _ in range(delay):
                if not high_activity[0]:
                    return
                time.sleep(0.1)
        mot.throttle = None
        for _ in range(random.choice([10,15,18,20])):
            if not high_activity[0]:
                return
            time.sleep(0.1)

if __name__ == '__main__':
    main_loop(2)