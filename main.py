#Main function / user interface
import pygame
import time
from classes import Button
from tic_tac_toe import *
from cpm import *
from pong import *
from sign_in import *
from platformer import *

#Setting up pygame and making all other required fonts, buttons, titles, if statement checkers, etc
pygame.init()
font = pygame.font.SysFont(None, 72)
game_selection_title = "Game Selection"
game_selection_title_surface = font.render(game_selection_title, True, "White")
main_title = "High Score Tracker"
main_title_surface = font.render(main_title, True, "White")

# Set the display mode to full-screen
screen = pygame.display.set_mode((2560, 1440))

clock = pygame.time.Clock()
start_button = Button(screen.get_width() / 2 - 200, 900, 300, 100, "Start", "Blue", "White")
exit_button = Button(screen.get_width() / 2 - 200, 1100, 300, 100, "Exit", "Blue", "White")
back_button = Button(screen.get_width() / 2 - 200, 1100, 300, 100, "Back", "Blue", "White")
tic_tac_button = Button(screen.get_width() / 2 - 200, 900, 300, 100, "Tic Tac Toe", "Purple", "White")
click_per_minute_button = Button(screen.get_width() / 2 + 300, 900, 300, 100, "Clicks Per Minute", "Red", "White")
pong_button = Button(screen.get_width() / 2 - 700, 900, 300, 100, "Pong", "Yellow", "White")
platformer_button = Button(screen.get_width() / 2 - 200, 700, 300, 100, "Platformer", "Green", "White")

def main():
    #Using sign in function to get the user to sign in or create an account
    username = sign_in_main(screen, clock)
    start_button_pressed = False
    running = True
    #The main game loop
    cpm_button_clicked = False
    pong_button_clicked = False
    platformer_button_clicked = False
    while running:
        #After every frame fill the screen the color black so that everything previous gets erased
        screen.fill("black")
        #Checking if the user decided to click the X if so quit pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Checking if the start button is pressed and if it is not load the main menu screen with the start and exit buttons while checking if they are pressed
        if start_button_pressed == False:
            screen.blit(main_title_surface, (screen.get_width() / 2 - 275, 500))
            start_button.draw(screen)
            exit_button.draw(screen)
            if start_button.is_clicked():
                #If the start button is pressed make the variable associated with it be true
                start_button_pressed = True
                time.sleep(0.2)
            if exit_button.is_clicked():
                #If the exit button is pressed exit the program
                running = False
        #If the start button is not pressed load the game selection menu with all its associated buttons by drawing them to the screen
        else:
            screen.blit(game_selection_title_surface, (screen.get_width() / 2 - 250, 500))
            back_button.draw(screen)
            #Multiple of these if statements appear where it checks if the button is being pressed this one sends you back to the main menu if pressed
            if back_button.is_clicked():
                start_button_pressed = False
                time.sleep(0.2)
            click_per_minute_button.draw(screen)
            #Sends you to clicks per minute game if clicks per minute button is pressed
            if click_per_minute_button.is_clicked():
                cpm(username, screen, clock)
                cpm_button_clicked = True
            #These if statements check to see if any buttons before the pong buttons have been pressed and if so make the pong button not be drawn
            if cpm_button_clicked == True:
                pass
            else:
                pong_button.draw(screen)
            #Sends you to pong game if pong button is clicked
            if pong_button.is_clicked():
                pong_loop(username, screen, clock)
                pong_button_clicked = True
            if cpm_button_clicked == True or pong_button_clicked == True:
                pass
            else:
                platformer_button.draw(screen)
            #Sends you to platformer game if platformer button is clicked
            if platformer_button.is_clicked():
                platformer_button_clicked = True
                platformer(username)
            if cpm_button_clicked == True or pong_button_clicked == True or platformer_button_clicked == True:
                pass
            else:
                tic_tac_button.draw(screen)
            if tic_tac_button.is_clicked():
                tic_tac_toe(username, screen, clock)
                screen.fill("black")
            cpm_button_clicked = False
            pong_button_clicked = False
            platformer_button_clicked = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

main()