import pygame
import random
import time
pygame.init()
 
# screen resolution
 
# opens up a window
 
# white color
color = (255,255,255)
 
# light shade of the button
color_light = (2,170,170)
 
# dark shade of the button
color_dark = (100,100,100)
 
# stores the width of the
# screen into a variable
 
# stores the height of the
# screen into a variable
 
# defining a font
smallfont = pygame.font.SysFont('Corbel',25)
 
# rendering a text written in
# this font
reaction_time = 0
wait_time1 = None
times = random.randint(3,9)






 


win = pygame.display.set_mode((2560,1385))
pygame.display.set_caption("First Game")


x = 10
y = 1320
width = 40
height = 40
vel = 5


isJump = False
jumpCount = 10


run = True


#place_x = random.randint(60, 1900)
#place_y = random.randint(1330, 1350)
#random_width = random.randint(40,120)
#random_hight = random.randint(40,100)
place_x = 60
place_y  = 1320
random_width = random.randint(40,120)
random_hight = random.randint(40,100)



while run:
    pygame.time.delay(20)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()
   
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel


    if keys[pygame.K_RIGHT] and x < 2560 - vel - width:  
        x += vel
    if x == place_x - 35 and y == place_y:
        print(place_y - random_hight)
        x -= vel
    if x == place_x + 290 and y == place_y:
        print(place_y)
        x += vel
  

    






       
    if not(isJump):




        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
            if y == place_y - 50:
                    y = place_y - 90
                    y = 1270





            
        else:
            jumpCount = 10
            isJump = False
   
    win.fill((0,0,0))
    pygame.draw.rect(win, (0,255,0), (x, y, width, height))
    for i in range(1,times):
            pygame.draw.rect(win, (255,0,0), (place_x, place_y, 300, 150))


 
   


    pygame.display.update()
   
pygame.quit()
