#Tic Tac Toe function / game
import pygame
import random
from classes import *

pygame.init()
screen = pygame.display.set_mode((2560, 1375))
clock = pygame.time.Clock()
tic_rect_1 = pygame.Rect((screen.get_width() / 2), (screen.get_height() / 2) - 240, 20, 340)
tic_rect_2 = pygame.Rect((screen.get_width() / 2) - 120, (screen.get_height() / 2) - 240, 20, 340)
tic_rect_3 = pygame.Rect((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 140, 340, 20)
tic_rect_4 = pygame.Rect((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 20, 340, 20)
tic_rect_list = [tic_rect_1, tic_rect_2, tic_rect_3, tic_rect_4]
tic_button_1 = Button((screen.get_width() / 2) - 220, (screen.get_height() / 2), 100, 100, "", "Black", "White")
tic_button_2 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2), 100, 100, "", "Black", "White")
tic_button_3 = Button((screen.get_width() / 2) + 20, (screen.get_height() / 2), 100, 100, "", "Black", "White")
tic_button_4 = Button((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 120, 100, 100, "", "Black", "White")
tic_button_5 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 120, 100, 100, "", "Black", "White")
tic_button_6 = Button((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 120, 100, 100, "", "Black", "White")
tic_button_7 = Button((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 240, 100, 100, "", "Black", "White")
tic_button_8 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 240, 100, 100, "", "Black", "White")
tic_button_9 = Button((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 240, 100, 100, "", "Black", "White")

def tic_tac_toe():
    running = True
    dt = 0
    tic_1_active = True
    tic_2_active = True
    tic_3_active = True
    tic_4_active = True
    tic_5_active = True
    tic_6_active = True
    tic_7_active = True
    tic_8_active = True
    tic_9_active = True
    tic_1_pl_pressed = False
    tic_2_pl_pressed = False
    tic_3_pl_pressed = False
    tic_4_pl_pressed = False
    tic_5_pl_pressed = False
    tic_6_pl_pressed = False
    tic_7_pl_pressed = False
    tic_8_pl_pressed = False
    tic_9_pl_pressed = False
    player_turn_over = False
    player_turn = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        for rect in tic_rect_list:
            pygame.draw.rect(screen, "White", rect)
        if player_turn:
            while player_turn_over == False:
                if tic_1_active:
                    tic_button_1.draw(screen)
                    if tic_button_1.is_clicked():
                        tic_1_active = False
                        tic_1_pl_pressed = True
                        player_turn = False
                        player_turn_over = True
        
        pygame.display.flip()
        dt = clock.tick(120) / 1000

tic_tac_toe()