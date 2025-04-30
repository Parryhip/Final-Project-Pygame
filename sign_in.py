#Final Project: Sign in function

#importing pygame and nessecary functions
import pygame
from leaderboard import *
from classes import Button

#initializing screen, and pygame 
pygame.init()
screen = pygame.display.set_mode((2560, 1375))
screen.fill((255,255,255))

#Allow holding keys
pygame.key.set_repeat(300, 30) 


#setting up the clock to keep track of time
clock = pygame.time.Clock()
time_event = pygame.USEREVENT + 1
pygame.time.set_timer(time_event, 1000)


#variable to run the main loop
run = True

#function to ge thte best size of font for a textbox
def get_best_font(text, max_width, max_height, max_font_size=45, min_font_size=10):
    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = pygame.font.Font(None, font_size)
        text_width, text_height = font.size(text)
        if text_width <= max_width and text_height <= max_height:
            return font
    return pygame.font.Font(None, min_font_size)

#function to sign in
def sign_in():
    #buttons for choices
    buttons = []
    sign_in_button = Button(1000, 1150, 250, 125, "Sign In", "green", "blue")
    sign_up_button = Button(1000, 1150, 250, 125, "Create New Account", "green", "blue")

    #textbox
    usr_inp_rect = pygame.Rect(200, 400, 320, 50)

    #clear the user's test
    usr_txt = ""

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    usr_txt = usr_txt[:-1]
                elif event.key == pygame.K_RETURN:
                    print("Entered text:", usr_txt)
                    usr_txt = ''
                else:
                    usr_txt += event.unicode

        #Clear screen
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, "yellow", usr_inp_rect)

        #getting the font size
        font = get_best_font(usr_txt, usr_inp_rect.w - 10, usr_inp_rect.h - 10)

        #rendering things on screen
        txt_surface = font.render(usr_txt, True, "black")
        screen.blit(txt_surface, (usr_inp_rect.x + 5, usr_inp_rect.y + 5))

        #updating screen
        pygame.display.flip()


sign_in()