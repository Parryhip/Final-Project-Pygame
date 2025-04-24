#Final project: Click Per Minute Game

#importing pygame and button class
import pygame
from classes import Button

#initializing pygame and its window
pygame.init()
screen = pygame.display.set_mode((2560, 1375))
screen.fill((255,255,255))

#setting up the clock to keep track of time
clock = pygame.time.Clock()
time_event = pygame.USEREVENT + 1
pygame.time.set_timer(time_event, 1000)



#variables to display time
font = pygame.font.SysFont('Arial', 30)



#function for the clicks per miute game
def cpm():
    #set the run variable to true to have a while True loop
    run = True

    #variables to display time
    font = pygame.font.SysFont('Arial', 30)

    #variable for tracking time in seconds
    seconds_left = 60

    #variables for clicks
    clicks = 0


    #main clicking loop
    while run:
        #clear screen
        screen.fill((255,255,255))

        #set variables
        display_time = f"Time Left to Click: {str(seconds_left)}".rjust(3)
        display_clicks = f"Clicks: {str(clicks)}".rjust(3)

        #surfaces
        time_surface = font.render(display_time, True, (0,0,0))
        clicks_surface = font.render(display_clicks, True, (0,0,0))

        #getting events and handling them
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == time_event:
                seconds_left -= 1
                display_time = f"Time Left to Click: {str(seconds_left)}".rjust(3)
                display_clicks = f"Clicks: {str(clicks)}".rjust(3)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1

        #putting surfaces on screen
        screen.blit(time_surface, (2250,10))
        screen.blit(clicks_surface, (10,10))

        pygame.display.flip()        
        clock.tick(60)
        if seconds_left == 0:
            screen.fill((255,255,255))
            break

    #after game loop
    while run:
        #clear screen
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


cpm()