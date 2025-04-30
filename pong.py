# Pong Game - Gabriel Crozier

import pygame
pygame.init()

from classes import Button

class better_button(Button):
    def __init__(self, x, y, width, height, text, color, hover_color, ):
        super().__init__(x, y, width, height, text, color, hover_color) # Figure out at homer

#initializing pygame's window
screen = pygame.display.set_mode((2560, 1375))
screen.fill((0,255,0))

#setting up the clock to keep track of time
clock = pygame.time.Clock()
time_event = pygame.USEREVENT + 1
pygame.time.set_timer(time_event, 1000)

while True:
    screen.fill("green")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()