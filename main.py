#Main function / user interface
import pygame
import time
from classes import Button
from tic_tac_toe import *
from cpm import *
from pong import *
from sign_in import *

pygame.init()
font = pygame.font.SysFont(None, 72)
game_selection_title = "Game Selection"
game_selection_title_surface = font.render(game_selection_title, True, "White")
main_title = "High Score Tracker"
main_title_surface = font.render(main_title, True, "White")
screen = pygame.display.set_mode((2560, 1375))
clock = pygame.time.Clock()
start_button = Button(screen.get_width() / 2 - 200, 900, 300, 100, "Start", "Blue", "White")
exit_button = Button(screen.get_width() / 2 - 200, 1100, 300, 100, "Exit", "Blue", "White")
back_button = Button(screen.get_width() / 2 - 200, 1100, 300, 100, "Back", "Blue", "White")
tic_tac_button = Button(screen.get_width() / 2 - 200, 900, 300, 100, "Tic Tac Toe", "Purple", "White")
click_per_minute_button = Button(screen.get_width() / 2 + 300, 900, 300, 100, "Clicks Per Minute", "Red", "White")
pong_button = Button(screen.get_width() / 2 - 700, 900, 300, 100, "Pong", "Yellow", "White")
platformer_button = Button(screen.get_width() / 2 - 700, 700, 300, 100, "Platformer", "Green", "White")
reaction_speed_button = Button(screen.get_width() / 2 + 300, 700, 300, 100, "Reaction Speed Test", "Red", "White")


def main():
    username = sign_in_main()
    start_button_pressed = False
    running = True
    while running:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if start_button_pressed == False:
            screen.blit(main_title_surface, (screen.get_width() / 2 - 275, 500))
            start_button.draw(screen)
            exit_button.draw(screen)
            if start_button.is_clicked():
                start_button_pressed = True
                time.sleep(0.2)
            if exit_button.is_clicked():
                running = False
        else:
            screen.blit(game_selection_title_surface, (screen.get_width() / 2 - 250, 500))
            back_button.draw(screen)
            if back_button.is_clicked():
                start_button_pressed = False
                time.sleep(0.2)
            click_per_minute_button.draw(screen)
            if click_per_minute_button.is_clicked():
                cpm(username, screen, clock)
            pong_button.draw(screen)
            if pong_button.is_clicked():
                pong_loop(username, screen, clock)
            platformer_button.draw(screen)
            if platformer_button.is_clicked():
                pass
            reaction_speed_button.draw(screen)
            if reaction_speed_button.is_clicked():
                pass
            tic_tac_button.draw(screen)
            if tic_tac_button.is_clicked():
                tic_tac_toe(username, screen, clock)
                screen.fill("black")
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

main()