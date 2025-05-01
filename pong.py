# Pong Game - Gabriel Crozier

import pygame
pygame.init()

from classes import Button

class better_button(Button):
    def __init__(self, x, y, width, height, text, color, hover_color, ):
        super().__init__(x, y, width, height, text, color, hover_color) # Figure out at homer


def main():
    #initializing pygame's window
    screen = pygame.display.set_mode((500, 500))
    screen.fill((0,0,0))

    #setting up the clock to keep track of time
    clock = pygame.time.Clock()
    time_event = pygame.USEREVENT + 1
    pygame.time.set_timer(time_event, 1000)

    brightness = 150

    run = [brightness,0,0]
    increase = 0.008

    pygame.draw.rect(pygame.Rect(screen.get_width()/2)) # WORK PLEASE

    while True:
        if run[0] >= brightness and run[1] < brightness:
            run[1] += increase
        if run[1] >= brightness and run[0] > 0:
            run[0] -= increase
        if run[1] >= brightness and run[2] < brightness:
            run[2] += increase
        if run[2] >= brightness and run[1] > 0:
            run[1] -= increase
        if run[2] >= brightness and run[0] < brightness:
            run[0] += increase
        if run[0] >= brightness and run[2] > 0:
            run[2] -= increase
        for i in range(3):
            if run[i] > brightness:
                run[i] = brightness
            elif run[i] < 0:
                run[i] = 0
        screen.fill((run[0],run[1],run[2]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.flip()

main()