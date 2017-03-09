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

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 10
DRY_RUN = False

pygame.init()

# Set the width and height of the screen [width,height]
# size = [500, 700]
# screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
arm = Arm(FPS, dry_run=DRY_RUN, verbose=True, velocity_scale=1000)
arm.go_home()

# is this entire mapping something ROS would help with?
BUTTON_GO_HOME = 9
# map from joystick axes to arm axes
JOYSTICK_AXES_MAP = {
    0: 3,
    1: 0,
    3: -2,
    4: 1,
}
# map from joystick axes to logical axes
LOGICAL_AXES_MAP = {
    0: 0,
    1: 1,
    3: 2,
    4: 3,
}


def sign(x):
    if sign > 0:
        return 1
    elif sign == 0:
        return 0
    else:
        return -1


def interact_with_arm():
    # apply this to all joysticks for now ...
    for joystick_id in range(pygame.joystick.get_count()):
        joystick = pygame.joystick.Joystick(joystick_id)
        joystick.init()

        arm.set_velocities({
            LOGICAL_AXES_MAP[joystick_axis]: (
                joystick.get_axis(joystick_axis) *
                sign(arm_axis)
            )
            for joystick_axis, arm_axis in JOYSTICK_AXES_MAP.items()
        })

        # start button triggers go home
        buttons = joystick.get_numbuttons()
        for button_id in range(buttons):
            if button_id == BUTTON_GO_HOME and joystick.get_button(button_id):
                arm.go_home()


def display_joystick_status():
    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    print("Number of joysticks: {}".format(joystick_count))

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        print("Joystick {}".format(i))

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        print("Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        print("Number of axes: {}".format(axes))

        for i in range(axes):
            axis_value = joystick.get_axis(i)
            print("Axis {} value: {:>6.3f}".format(i, axis_value))

        buttons = joystick.get_numbuttons()
        print("Number of buttons: {}".format(buttons))

        for i in range(buttons):
            button = joystick.get_button(i)
            print("Button {:>2} value: {}".format(i, button))

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        print("Number of hats: {}".format(hats))

        for i in range(hats):
            hat = joystick.get_hat(i)
            print("Hat {} value: {}".format(i, str(hat)))


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


# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN
        # JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # display_joystick_status()
    interact_with_arm()

    # Limit to 60 frames per second
    clock.tick(FPS)

    display_measured_fps()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
