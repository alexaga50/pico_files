from machine import Pin, SPI
from sh1106 import SH1106_SPI
import framebuf
from utime import sleep
#import screen


# pins: 4=res(GP2),6=cs(GP4),7=dc(GP5),14=clk(GP10),15=mosi(GP11),vcc,GND


spi = SPI(1, baudrate=1000000)
display = SH1106_SPI(128, 64, spi, Pin(5), Pin(2), Pin(4))
#display.flip(90)
display.sleep(False)

x=128
y=64
ball_sise=8
x_Pos = 10
y_Pos = 15
x_Vel = -1
y_Vel = 1

while True:
    display.fill(0)
    display.rect(x_Pos, y_Pos,ball_sise,ball_sise, 1)
    
    x_Pos += x_Vel#κίνηση της μπάλας στον άξονα x
    y_Pos += y_Vel#κίνηση της μπάλας στον άξονα y
    if x_Pos > x-ball_sise or x_Pos <1:#από το τέλος του άξονα x αφαιρείται το μέγεθος της μπάλας
        x_Vel *= -1
    if y_Pos >y-ball_sise or y_Pos <1:#από το τέλος του άξονα y αφαιρείται το μέγεθος της μπάλας
        y_Vel *= -1
    display.show()
    #sleep(0.001)