from machine import Pin, SPI
from sh1106 import SH1106_SPI
import framebuf
from time import sleep
import urandom


#import screen
# pins: 4=res(GP16),6=cs(GP18),7=dc(GP17),14=clk(GP10),15=mosi(GP11),vcc,GND
# pins: dc(GP17),res(GP16),cs(GP18),clk(GP10),mosi(GP11),vcc,GND

spi = SPI(1, baudrate=1000000)
oled = SH1106_SPI(128, 64, spi, Pin(17), Pin(16), Pin(18))
#display.flip(90)
oled.sleep(False)


button_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

# Game variables
bird_pos = [30, 30]
bird_velocity = 0
gravity = 0.2
jump_strength = -2
game_over = False
score = 0

# Pipe variables
pipe_width = 10
pipe_height = 20
pipe_gap = 30
pipe_distance = 60
pipe_speed = 1
pipe_pos = [127, 1]
pipe_passed = False

# Button variables
button_state = False

# Clear screen
oled.fill(0)
oled.show()

def draw_bird():
    oled.fill_rect(bird_pos[0], bird_pos[1], 4, 4, 1)

def draw_pipe():
    oled.fill_rect(pipe_pos[0], 0, pipe_width, pipe_pos[1], 1)
    oled.fill_rect(pipe_pos[0], pipe_pos[1] + pipe_gap, pipe_width, oled.height - (pipe_pos[1] + pipe_gap), 1)

def update_bird():
    global bird_pos, bird_velocity, game_over

    bird_velocity += gravity
    bird_pos[1] += int(bird_velocity)

    if bird_pos[1] < 0:
        bird_pos[1] = 0
        bird_velocity = 0

    if bird_pos[1] > oled.height - 4:
        bird_pos[1] = oled.height - 4
        game_over = True
        reset_game()  # Call reset_game() function when the bird touches the ground

def update_pipe():
    global pipe_pos, pipe_passed, score

    pipe_pos[0] -= pipe_speed

    if pipe_pos[0] < -pipe_width:
        pipe_pos[0] = oled.width
        pipe_pos[1] = urandom.randint(8, oled.height - pipe_gap - 8)
        pipe_passed = False
        score += 1

def handle_buttons():
    global button_state

    button_state = button_pin.value() == 0

def check_collision():
    if bird_pos[0] + 4 > pipe_pos[0] and bird_pos[0] < pipe_pos[0] + pipe_width:
        if bird_pos[1] < pipe_pos[1] or bird_pos[1] + 4 > pipe_pos[1] + pipe_gap:
            return True
    if bird_pos[1] < 0 or bird_pos[1] + 4 > oled.height:
        return True
    return False

def reset_game():
    global bird_pos, bird_velocity, game_over, score, pipe_pos, pipe_passed

    bird_pos = [32, 32]
    bird_velocity = 0
    game_over = False
    score = 0
    pipe_pos = [127, 1]
    pipe_passed = False

# Game loop
while True:
    oled.fill(0)

    handle_buttons()

    if button_state:
        bird_velocity = jump_strength

    update_bird()
    update_pipe()

    if check_collision():
        reset_game()

    draw_pipe()
    draw_bird()

    # Display score in bottom right corner
    score_text = str(score) + " "
    score_x = oled.width - len(score_text) * 6
    score_y = oled.height - 8
    oled.text(score_text, score_x, score_y)

    oled.show()
    sleep(0.01)
