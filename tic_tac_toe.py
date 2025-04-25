#Tic Tac Toe function / game
import pygame
import random
from classes import *

pygame.init()
screen = pygame.display.set_mode((2560, 1375))
clock = pygame.time.Clock()
tic_button_2 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2), 100, 100, "", "White", "White")
tic_button_5 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 100, 100, 100, "", "White", "White")

running = True
dt = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    tic_button_5.draw(screen)
    tic_button_2.draw(screen)
    pygame.display.flip()
    dt = clock.tick(120) / 1000