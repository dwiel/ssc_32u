"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Show everything we can pull off the joystick
"""
import pygame
import time
import math
from ssc_32u.arm import Arm
from evdev import InputDevice, list_devices, ecodes, categorize, events

FPS = 10
DRY_RUN = False

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
devices = [InputDevice(fn) for fn in list_devices()]
assert len(devices) == 1
dev = devices[0]

# Get ready to print
arm = Arm(FPS, dry_run=DRY_RUN, verbose=True, velocity_scale=1000)
arm.go_home()

# is this entire mapping something ROS would help with?
BUTTON_GO_HOME = 9
# map from joystick axes to (arm_axis, sign)
JOYSTICK_AXES_MAP = {
    0: (3, 1),
    1: (0, 1),
    3: (2, -1),
    4: (1, 1),
}


def interact_with_arm(velocities):
    arm.set_velocities({
        abs(arm_axis): velocities.get(joystick_axis, 0) * sign
        for joystick_axis, (arm_axis, sign) in JOYSTICK_AXES_MAP.items()
    })

    # # start button triggers go home
    # buttons = joystick.get_numbuttons()
    # for button_id in range(buttons):
    #     if button_id == BUTTON_GO_HOME and joystick.get_button(button_id):
    #         arm.go_home()


steps = 0
old_clock = time.clock()


def display_measured_fps():
    global steps
    global old_clock

    steps += 1
    if steps % 100 == 0:
        new_clock = time.clock()
        print(100 / (new_clock - old_clock))
        old_clock = new_clock

print(dev.capabilities(verbose=True))

# -------- Main Program Loop -----------
import threading


class JoystickThread(threading.Thread):
    def __init__(self):
        super(JoystickThread, self).__init__()

        # {joystick_axis: velocity (-1.0, 1.0)}
        self.state = {}

    def run(self):
        for event in dev.read_loop():
            time_delta = event.timestamp() - time.time()

            if time_delta > 0.1:
                print("warning: time delay: %.04f" % time_delta)

            if event.type == 0:
                if all(v > -3/128.0 and v < 3/128.0 for v in self.state.values()):
                    continue
            elif event.type == 3:
                self.state[event.code] = (event.value - 128) / 128.0

            event = categorize(event)
            if isinstance(event, events.KeyEvent):
                if event.keystate == events.KeyEvent.key_down:
                    if event.event.code == 297:
                        arm.go_home()


joystick = JoystickThread()
joystick.daemon = True
joystick.start()

while True:
    # send state
    print('send', joystick.state)
    interact_with_arm(joystick.state)

    # limit frames per second
    clock.tick(FPS)

    display_measured_fps()
