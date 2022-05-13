
import board
i2c = board.I2C()

import time
import random

# 71, 72, 76

COLOR_MASK = [
    [0b00000000,0b00000000],
    [0b11111111,0b00000000],
    [0b00000000,0b11111111],
    [0b11111111,0b11111111],
]

class Display:

    def __init__(self,i2c,address):
        self._buffer = [0]*16
        self._i2c = i2c
        self._address = address
        self._i2c.writeto(address, bytes([0x21]) ) # 0010_xxx1 Turn the oscillator on
        self._i2c.writeto(address, bytes([239]) ) # 1110_1111 Full brightness
        self._i2c.writeto(address, bytes([0b10000001]) ) # 1000_x001 Blinking off, display on        
        self.clear()
        self.refresh()        

    @staticmethod
    def text_to_bytes(s):
        s = s.replace('.','9')
        s = s.replace('+','0')
        s = s.replace(' ','')
        ds = s.strip().split()
        data = []
        for d in ds:
            row = []
            for c in d:
                row.append(int(c))
            data.append(row)
        return data

    def test(self):
        self._i2c.writeto(self._address, bytes([0, 1,0,0,2,4,4]) )

    def clear(self,c=0):        
        v = COLOR_MASK[c]
        self._buffer = [v[0],v[1]]*8

    def refresh(self):
        self._i2c.writeto(self._address, bytes([0]+self._buffer) )

    def draw_image(self,data,dx,dy):        
        for y in range(8):
            for x in range(8):
                c = data[y+dy][x+dx]
                if c<4:
                    self.set_pixel(x,y,data[y+dy][x+dx])

    def set_pixel(self, x, y, color):
        """
            color is 0=black, 1=green, 2=red, 3=yellow
            binary: 00=black, 01=green, 10=red, and 11=yellow
        """
        pos = 7-x
        pos = pos * 2
        
        bit = 1<<y # All 0s with a single 1
        mask = ~bit # All 1s with a single 0
        
        # Decode the color value into separate bits
        color_g = color & 1
        color_r = (color & 2) >> 1
        
        if color_g:
            self._buffer[pos] = self._buffer[pos] | bit
        else:
            self._buffer[pos] = self._buffer[pos] & mask
        
        if color_r:
            self._buffer[pos+1] = self._buffer[pos+1] | bit
        else:
            self._buffer[pos+1] = self._buffer[pos+1] & mask

# Spacing to support individual scrolls
TEXT_F = '''
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ++++++++ ........
........ ++33333+ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++3333++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++++++++ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
'''

TEXT_L = '''
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ++++++++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++3+++++ ........
........ ++33333+ ........
........ ++++++++ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
........ ........ ........
'''

# For all-three scrolling
TEXT_FLL = '''
........ ........ ........ ++$$$$$+ ++#+++++ ++@+++++ ........ ........ ........
........ ........ ........ ++$+++++ ++#+++++ ++@+++++ ........ ........ ........
........ ........ ........ ++$+++++ ++#+++++ ++@+++++ ........ ........ ........
........ ........ ........ ++$$$$++ ++#+++++ ++@+++++ ........ ........ ........
........ ........ ........ ++$+++++ ++#+++++ ++@+++++ ........ ........ ........
........ ........ ........ ++$+++++ ++#+++++ ++@+++++ ........ ........ ........
........ ........ ........ ++$+++++ ++#####+ ++@@@@@+ ........ ........ ........
........ ........ ........ ++++++++ ++++++++ ++++++++ ........ ........ ........
'''

SCROLLS_ON = [
    # X,Y  dX,dY      
    [ 1, 8,  1,  0], # LEFT
    [ 8, 1,  0,  1], # UP
    [15, 8, -1,  0], # RIGHT
    [ 8,15,  0, -1], # DOWN
]

SCROLLS_OFF = [
    # X,Y  dX,dY  
    [ 9, 8,  1,  0], # LEFT
    [ 8, 9,  0,  1], # UP
    [ 7, 8, -1,  0], # RIGHT
    [ 8, 7,  0, -1], # DOWN
]

LETTER_F = [
    Display.text_to_bytes(TEXT_F.replace('3','1')),
    Display.text_to_bytes(TEXT_F.replace('3','2')),
    Display.text_to_bytes(TEXT_F),
]

LETTER_L = [
    Display.text_to_bytes(TEXT_L.replace('3','1')),
    Display.text_to_bytes(TEXT_L.replace('3','2')),
    Display.text_to_bytes(TEXT_L),
]

d1 = Display(i2c,0x76)
d2 = Display(i2c,0x72)
d3 = Display(i2c,0x71)

def main_loop(high_activity):
    while True:
        _loop(high_activity)
        d1.clear()
        d2.clear()
        d3.clear()
        d1.refresh()
        d2.refresh()
        d3.refresh()
        while not high_activity[0]:
            time.sleep(0.25)

def _loop(high_activity):    
    while True:

        for j in range(0,64,4):
            d1.clear()
            d2.clear()
            d3.clear()
            for i in range(j):
                if not high_activity[0]:
                    return
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d1.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d2.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d3.set_pixel(x,y,c)
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        for j in range(64,0,-4):
            d1.clear()
            d2.clear()
            d3.clear()
            for i in range(j):
                if not high_activity[0]:
                    return
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d1.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d2.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d3.set_pixel(x,y,c)
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        d1.clear()
        d2.clear()
        d3.clear()
        d1.refresh()
        d2.refresh()
        d3.refresh()

        t = TEXT_FLL.replace('$','1').replace('#','2').replace('@','3')
        d = Display.text_to_bytes(t)
        for x in range(48,24,-1):
            if not high_activity[0]:
                    return
            d1.draw_image(d,x,0)
            d2.draw_image(d,x+8,0)
            d3.draw_image(d,x+16,0)
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        time.sleep(5)

        for x in range(24,0,-1):
            if not high_activity[0]:
                    return
            d1.draw_image(d,x,0)
            d2.draw_image(d,x+8,0)
            d3.draw_image(d,x+16,0)
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        for _ in range(10):
            if not high_activity[0]:
                return
            time.sleep(0.1)

        for j in range(0,64,4):
            d1.clear()
            d2.clear()
            d3.clear()
            for i in range(j):
                if not high_activity[0]:
                    return
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d1.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d2.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d3.set_pixel(x,y,c)
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        for j in range(64,0,-4):
            d1.clear()
            d2.clear()
            d3.clear()
            for i in range(j):
                if not high_activity[0]:
                    return
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d1.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d2.set_pixel(x,y,c)
                x = random.randint(0,7)
                y = random.randint(0,7)
                c = random.randint(1,3)
                d3.set_pixel(x,y,c)
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        d1.clear()
        d2.clear()
        d3.clear()
        d1.refresh()
        d2.refresh()
        d3.refresh()

        ca = random.randint(0,2)
        cb = random.randint(0,2)
        cc = random.randint(0,2)

        a = random.choice(SCROLLS_ON)
        b = random.choice(SCROLLS_ON)
        c = random.choice(SCROLLS_ON)
        for i in range(8):
            if not high_activity[0]:
                    return
            d1.draw_image(LETTER_F[ca],a[0]+i*a[2],a[1]+i*a[3])
            d2.draw_image(LETTER_L[cb],b[0]+i*b[2],b[1]+i*b[3])
            d3.draw_image(LETTER_L[cc],c[0]+i*c[2],c[1]+i*c[3])
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

        for _ in range(20):
            if not high_activity[0]:
                return
            time.sleep(0.1)

        a = random.choice(SCROLLS_OFF)
        b = random.choice(SCROLLS_OFF)
        c = random.choice(SCROLLS_OFF)
        for i in range(8):
            if not high_activity[0]:
                    return
            d1.draw_image(LETTER_F[ca],a[0]+i*a[2],a[1]+i*a[3])
            d2.draw_image(LETTER_L[cb],b[0]+i*b[2],b[1]+i*b[3])
            d3.draw_image(LETTER_L[cc],c[0]+i*c[2],c[1]+i*c[3])
            d1.refresh()
            d2.refresh()
            d3.refresh()
            time.sleep(0.1)

if __name__ == '__main__':
    main_loop()