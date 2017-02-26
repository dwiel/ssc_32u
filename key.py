import pygame
import sys
import arm

white = (255, 255, 255)
red = (255, 0, 0)

pygame.init()
pygame.display.set_caption('Keyboard Example')
size = [500, 500]
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

x = 0.5
y = 0.5
z = 0.5
wrist = 0.5
grip = 0.5

# using this to set the size of the rectange
# using this to also move the rectangle
step = 0.04

# by default the key repeat is disabled
# call set_repeat() to enable it
pygame.key.set_repeat(50, 50)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # check if key is pressed
        # if you use event.key here it will give you error at runtime
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= step
                arm.set_scaled_position(0, x)
            if event.key == pygame.K_RIGHT:
                x += step
                arm.set_scaled_position(0, x)
            if event.key == pygame.K_UP:
                y -= step
                arm.set_scaled_position(1, y)
            if event.key == pygame.K_DOWN:
                y += step
                arm.set_scaled_position(1, y)
            # previous page key
            if event.scancode == 166:
                z -= step
                arm.set_scaled_position(2, z)
            # next page key
            if event.scancode == 167:
                z += step
                arm.set_scaled_position(2, z)
            # ;
            if event.key == 39:
                wrist -= step
                arm.set_scaled_position(3, wrist)
            # '
            if event.key == 59:
                wrist += step
                arm.set_scaled_position(3, wrist)
            # .
            if event.key == 46:
                grip -= step
                arm.set_scaled_position(4, grip)
            # /
            if event.key == 47:
                grip += step
                arm.set_scaled_position(4, grip)
            print event.key

            # checking if left modifier is pressed
            if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                if event.key == pygame.K_LEFT:
                    x = 0
                if event.key == pygame.K_RIGHT:
                    x = 500 - step
                if event.key == pygame.K_UP:
                    y = 0
                if event.key == pygame.K_DOWN:
                    y = 500 - step

    # limit the rectangle from going out of the visible area
    if (x < 0): x = 0
    elif (x > (500-step)): x = 500-step
    if (y < 0): y = 0
    elif (y > (500-step)): y = 500-step
    if (z < 0): z = 0
    elif (z > (500-step)): z = 500-step
    if (grip < 0): grip = 0
    elif (grip > (500-step)): grip = 500-step
    if (wrist < 0): wrist = 0
    elif (wrist > (500-step)): wrist = 500-step


    screen.fill(white)

    # draw a rectangle
    pygame.draw.rect(screen, red, ((x*500, y*500), (step*500, step*500)), 0)

    pygame.display.update()
    clock.tick(20)
