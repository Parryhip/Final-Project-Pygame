#Main function / user interface
import pygame
import time
from tic_tac_toe import tic_tac_toe
from classes import Button

pygame.init()
screen = pygame.display.set_mode((2560, 1375))
clock = pygame.time.Clock()
start_button = Button(screen.get_width() / 2 - 100, 900, 200, 100, "Start", "Blue", "White")
exit_button = Button(screen.get_width() / 2 - 100, 1100, 200, 100, "Exit", "Blue", "White")
back_button = Button(screen.get_width() / 2 - 100, 1100, 200, 100, "Back", "Blue", "White")
tic_tac_button = Button(screen.get_width() / 2 - 100, 900, 200, 100, "Tic Tac Toe", "Purple", "White")

def main():
    start_button_pressed = False
    running = True
    dt = 0
    while running:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if start_button_pressed == False:
            start_button.draw(screen)
            exit_button.draw(screen)
            if start_button.is_clicked():
                start_button_pressed = True
                time.sleep(0.1)
            if exit_button.is_clicked():
                running = False
        else:
            back_button.draw(screen)
            if back_button.is_clicked():
                start_button_pressed = False
                time.sleep(0.1)
            tic_tac_button.draw(screen)
            if tic_tac_button.is_clicked():
                tic_tac_toe("tom")
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    pygame.quit()

main()