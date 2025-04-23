#Final project: Click Per Minute Game

#importing pygame
import pygame

#initializing pygame and its window
pygame.init()
screen = pygame.display.set_mode((2562, 1340))

#setting up the clock to keep track of time
clock = pygame.time.Clock()
time_event = pygame.USEREVENT + 1
pygame.time.set_timer(time_event, 1000)


#variable for tracking time in seconds
seconds_left = 60

#variables to display time
font = pygame.font.SysFont('Consolas', 10)
display_time = '60'.rjust(3)

#set the run variable to true to have a while True loop
run = True

#function for the clicks per miute game
def cpm():
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.blit(display_time, True, (0,0,0), (25,5))
        pygame.display.flip()        
        clock.tick(60)

cpm()