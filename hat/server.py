import aiohttp
from aiohttp import web
import logging

import board
from adafruit_motorkit import MotorKit

kit = MotorKit(i2c=board.I2C())
motors = [kit.motor1,kit.motor2,kit.motor3,kit.motor4]

LOGGER = logging.getLogger(__name__)

async def control_handler(request):
    action = request.match_info.get('action', '')
    motor,speed = action.split('-')

    print('##',motor,speed)

    motor = motors[int(motor)]

    print('##',motor)
    
    if speed=='COAST':
        speed = None
    else:
        speed = int(speed)
    print(f'Setting {motor} to {speed}')
    motor.throttle = speed/100 

    text = f'Requested action {action}'
    return web.Response(text=text)

async def app_factory():
    app = web.Application()    
    app.add_routes([
        web.get('/control/{action}',control_handler),              
        web.static('/','webroot'),
    ])    
    return app

if __name__ == '__main__':

    logging.basicConfig(level='DEBUG')           
    web.run_app(app_factory(),port=80)    
