#Final project: Click Per Minute Game

#importing/initializing pygame, button class, and getting leaderboard functions
import pygame
pygame.init()
from classes import Button
from leaderboard import *

#importing csv
import csv

#initializing pygame's window
screen = pygame.display.set_mode((2560, 1375))
screen.fill((255,255,255))

#setting up the clock to keep track of time
clock = pygame.time.Clock()
time_event = pygame.USEREVENT + 1
pygame.time.set_timer(time_event, 1000)



#variables to display time
font = pygame.font.SysFont('Arial', 30)



#function for the clicks per miute game
def cpm(username):
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

        #updates screen
        pygame.display.flip()    

        #frame rate    
        clock.tick(60)

        #if the time is up
        if seconds_left == 0:
            #clear screen
            screen.fill((255,255,255))
            pygame.display.flip()
            break

    #list for all buttons
    cpm_buttons = []

    #initilaizing buttons and add them to the list of all buttons
    cpmleaderboardbutton = Button(2250, 1150, 250, 125, "Go to Leaderboard", "green", "blue")
    go_back_to_main_screen = Button(50, 1150, 250, 125, "Game Selection", "green", "blue")
    cpm_buttons.append(cpmleaderboardbutton)
    cpm_buttons.append(go_back_to_main_screen)


    #after game loop
    while run:
        #clear screen
        screen.fill((255,255,255))

        #setting to not breakout yet
        breakout = False

        #checking events
        for event in pygame.event.get():
            #checking if user wants to quit using X button
            if event.type == pygame.QUIT:
                #quit
                run = False
            
            #checking events of buttons
            for button in cpm_buttons:
                returnvalue = button.is_clicked()
                if returnvalue:
                    if button == go_back_to_main_screen:
                        return
                    else:
                        breakout = True
                    break
            if breakout:
                break
        
        #if user is going to leaderboard:
        if breakout:
            gotoleaderboard = True
            break

        #drawing buttons 
        for button in cpm_buttons:
            button.draw(screen)

        #update screen
        pygame.display.flip()

        #frame_rate
        clock.tick(60)

    
    #getting the old cpm score for comparison
    get_score(username, 1)

    #inputting the new score
    input_score(username, 1, clicks)

    #getting the leaderboard
    cpmleaderboard = get_leaderboard(1)

    #removing the old buttons except for the going back to main screen button
    cpm_buttons.clear()
    cpm_buttons.append(go_back_to_main_screen)

    #going to leaderboard loop
    while run:
        #clear screen
        screen.fill((255,255,255))

        #score surfaces
        scoresurfaces = []

        #show leaderboard!
        cpm_leaderboard_title = "----------TOP 10 CPM SCORES----------"
        
        #surfaces
        title_surface = font.render(cpm_leaderboard_title, True, (0,0,0))

        num = 1

        for score in cpmleaderboard:
            scoresurfaces.append(font.render(f"{num}. {score[0]}: {score[1]}", True, (0,0,0)))
            num += 1


        for event in pygame.event.get():
            #checing if the user clicked the X button
            if event.type == pygame.QUIT:
                run = False
            #checking events of buttons
            for button in cpm_buttons:
                returnvalue = button.is_clicked()
                if returnvalue:
                    if button == go_back_to_main_screen:
                        return

        #variable for showing first score
        position = (1000, 500)

        #surface showing
        screen.blit(title_surface, (1000, 470))
        for surface in scoresurfaces:
            screen.blit(surface, position)
            position = (1000, position[1] + 30)

        for button in cpm_buttons:
            button.draw(screen)

        #updating displays
        pygame.display.flip()

        #setting frame_rate
        clock.tick(60)

#calling of clicks per minute function (remove at the end!)
cpm("tim")