# Lego Hat
For FLL Events

# Parts

Foam:<br>
https://www.amazon.com/gp/product/B00069PFKK

Motors:<br>
https://www.amazon.com/gp/product/B00VUC7MQW

Motor Controller:<br>
https://www.adafruit.com/product/4280

Gears:<br>
https://www.amazon.com/gp/product/B01LVXYZ9L

Small Displays:<br>
https://www.ebay.com/itm/2-4-240x320-SPI-TFT-LCD-Serial-Port-Module-3-3V-PCB-Adapter-SD-ILI9341/321496984303


# Construction

![](art/hat-foam1.jpg)

![](art/hat-foam2.jpg)

```
sudo pip3 install adafruit-circuitpython-motorkit

from adafruit_motorkit import MotorKit
kit = MotorKit()

kit.motor1.throttle = 1.0
kit.motor3.throttle = 1.0

```
