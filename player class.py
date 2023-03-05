from machine import Pin, SPI
from sh1106 import SH1106_SPI
import framebuf
from utime import sleep

t=0.05
xy = 8
wx = 40
wy = 8



spi = SPI(1, baudrate=1000000)
display = SH1106_SPI(128, 64, spi, Pin(17), Pin(16), Pin(18))
#display.flip(90)
display.sleep(False)

man=[0x18, 0x24, 0x18, 0x3c, 0x5a, 0x18, 0x24, 0x24]
wall=[0x00, 0x7e, 0x02, 0x76, 0x76, 0x40, 0x7e, 0x00]


buff1 = bytearray(wall)
buff2 = bytearray(man)

fb1 = framebuf.FrameBuffer(buff1,xy,xy, framebuf.MONO_HLSB)
fb2 = framebuf.FrameBuffer(buff2,xy,xy, framebuf.MONO_HLSB)

display.fill(0)

pin0 = Pin(0, Pin.IN,Pin.PULL_UP)#right button 2
pin1 = Pin(1, Pin.IN,Pin.PULL_UP)#left button 1 
pin2 = Pin(2, Pin.IN,Pin.PULL_UP)#down button 3
pin3 = Pin(3, Pin.IN,Pin.PULL_UP)#up button 4

def wall_tile(x, y):
    display.blit(fb1,x,y)


class Player:
    
    def __init__(self,x,y,h,w):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        
    def player_move(self):
        if pin1.value()==0 :self.x += self.w #right
        if pin0.value() ==0:self.x -= self.w#left
        if pin2.value()==0:self.y += self.h #down
        if pin3.value()==0:self.y -= self.h #Up
        if self.y<8:self.y=8
        if self.y>54:self.y=54
        if self.x<0:self.x=0
        if self.x>120:self.x=120
        
        display.blit(fb2,self.x,self.y)
   
    def update_move(self):#χρειάζεται αυτό να μήν αφήνει σκιές ο παίκτης
        display.fill_rect(self.x,self.y,self.w,self.h,0)
        sleep(t)


player = Player(0,0,8,8)


while True:
    
    Player.update_move(player)
    Player.player_move(player)
    sleep(t)
    display.show()
 