

import csv
import pygame
import sys
import time
import random
 
# initializing the constructor
pygame.init()
 
# screen resolution
res = (2560,1375)
 
# opens up a window
screen = pygame.display.set_mode(res)
 
# white color
color = (255,255,255)
 
# light shade of the button
color_light = (170,170,170)
 
# dark shade of the button
color_dark = (100,100,100)
 
# stores the width of the
# screen into a variable
width = screen.get_width()
 
# stores the height of the
# screen into a variable
height = screen.get_height()
 
# defining a font
smallfont = pygame.font.SysFont('Corbel',25)
 
# rendering a text written in
# this font
reaction_time = 0
wait_time1 = None
wait_time1 = random.randint(1,9)
time.sleep(wait_time1)
text = smallfont.render('Click!' , True , color)
click = False
score = None
random_pop = random.randint(1,5)



while True:

    
     
    reaction_time += 0.1
    time.sleep(0.1)
    for ev in pygame.event.get():
               
            #checks if a mouse is clicked
            if ev.type == pygame.MOUSEBUTTONDOWN:
               
               
                #if the mouse is clicked on the
                # button the game is terminated
                    if width/2 <= mouse[0] <= width/random_pop and height/2 <= mouse[1] <= height/2+40 and click == False:
                        text = smallfont.render(f'Your reaction time is {round(reaction_time*1000,2)} MS\npress q to quit, and r to restart\n(after pressing r to play again, wait \nuntil the message turns to : Click!) \n' , True , color)
                        score = reaction_time
                        click = True
                        print(score)







                     
                     
       
            if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_q:
                         pygame.quit()
                         sys.exit()
                    elif ev.key == pygame.K_r:
                        try:    
                            # initializing the constructor
                            pygame.init()

                            # screen resolution
                            res = (2560,1375)

                            # opens up a window
                            screen = pygame.display.set_mode(res)

                            # white color
                            color = (255,255,255)

                            # light shade of the button
                            color_light = (170,170,170)

                            # dark shade of the button
                            color_dark = (100,100,100)

                            # stores the width of the
                            # screen into a variable
                            width = screen.get_width()

                            # stores the height of the
                            # screen into a variable
                            height = screen.get_height()

                            # defining a font
                            smallfont = pygame.font.SysFont('Corbel',25)
                            reaction_time = 0
                            score = 0
                            wait_time1 = None
                            wait_time1 = random.randint(1,9)
                            time.sleep(wait_time1)
                            text = smallfont.render('Click!' , True , color)
                            click = False
                            score = None
                            random_place = True
                            if random_place == True:
                                 random_pop = random.randint(1,5)
                        except TypeError:
                              reaction_time = 1000000
                              text = smallfont.render(f'You clicked before it tells you to\n,cheating will end up with a super \nhigh reaction time! your \nreaction is {round(reaction_time*1000,2)} MS\n press q to quit, and r to play again' , True , color)
                             
             






    # fills the screen with a color
    screen.fill((100,25,60))
     
    # stores the (x,y) coordinates into
    # the variable as a tuple
    mouse = pygame.mouse.get_pos()
     
    # if mouse is hovered on a button it
    # changes to lighter shade  


    if width/2 <= mouse[0] <= width/random_pop and height/2 <= mouse[1] <= height/2+40:
        pygame.draw.rect(screen,color_light,[width/random_pop,height/2,200,40])
         
    else:
        pygame.draw.rect(screen,color_dark,[width/random_pop,height/2,200,40])
     
    # superimposing the text onto our button
    screen.blit(text , (width/2+300,height/2))
     
    # updates the frames of the game
    pygame.display.update()
