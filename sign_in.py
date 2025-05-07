#Final Project: Sign in function

#importing pygame and nessecary functions
import pygame
from leaderboard import *
from classes import Button
import bcrypt

#initializing screen, and pygame
pygame.init()
screen = pygame.display.set_mode((2560, 1375))
screen.fill((255,255,255))
normal_font = pygame.font.SysFont("Arial", 32)

#Allow holding keys
pygame.key.set_repeat(300, 30) 


#setting up the clock to keep track of time
clock = pygame.time.Clock()
time_event = pygame.USEREVENT + 1
pygame.time.set_timer(time_event, 1000)


#variable to run the main loop
run = True

#function to ge thte best size of font for the textbox
def get_best_font(text, max_width, max_height, max_font_size=45, min_font_size=10):
    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = pygame.font.Font(None, font_size)
        text_width, text_height = font.size(text)
        if text_width <= max_width and text_height <= max_height:
            return font
    return pygame.font.Font(None, min_font_size)

#function to check if username matches any of the ones in the files prior
def check_username(username):
    with open("signin.txt", "r") as file:
        for line in file:
            splitline = line.split(",")
            if username == splitline[0]:
                return False
            else:
                pass
        
        return True

#function to sign in
def sign_in():
    #buttons for choices
    buttons = []
    sign_in_button = Button(500, 1150, 250, 125, "Sign In", "green", "blue")
    sign_up_button = Button(1500, 1150, 250, 125, "Create New Account", "green", "blue")

    #add buttons to the list
    buttons.append(sign_in_button)
    buttons.append(sign_up_button)

    #setting not to break yet or go to the sign_in/sign_up steps
    signin = False
    signup = False
    breakout = False

    #loop for button selections
    while run:
        #clear screen
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for button in buttons:
                if button.is_clicked():
                    if button == sign_in_button:
                        signin = True
                        breakout = True
                        break
                    elif button == sign_up_button:
                        signup = True
                        breakout = True
                        break
            if breakout:
                break
        if breakout:
            break

        #drawing buttons
        for button in buttons:
            button.draw(screen)

        #update screen
        pygame.display.flip()

        #frame rate
        clock.tick(60)


    #textbox
    usr_inp_rect = pygame.Rect(0,0, 320, 50)

    #centering textbox
    usr_inp_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    #clear the user's textbox
    usr_txt = ""

    #text to show where to input stuff
    usernametitle = "Username:"
    passwordtitle = "Password:"
    newusernametitle = "Create new username:"
    newpasswordtitle = "Create new password:"
    confpasswordtitle = "Confirm new password:"

    if signin:
        username_rect = pygame.Rect(screen.get_width() // 2 - 160, 600, 320, 50)
        password_rect = pygame.Rect(screen.get_width() // 2 - 160, 700, 320, 50)

        username_active = False
        password_active = False

        #text to show in the text boxes
        username_text = ""
        password_text = ""

        #setting up the cursor diplay on the text box
        cursor_visible = True
        cursor_timer = 0
        cursor_interval = 500  #in milliseconds

        while run:
            dt = clock.tick(60)
            cursor_timer += dt
            if cursor_timer >= cursor_interval:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        username_active = True
                        password_active = False
                    elif password_rect.collidepoint(event.pos):
                        password_active = True
                        username_active = False
                    else:
                        username_active = False
                        password_active = False

                if event.type == pygame.KEYDOWN:
                    if username_active:
                        if event.key == pygame.K_BACKSPACE:
                            username_text = username_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            inputtedusername = username_text
                        else:
                            username_text += event.unicode
                    elif password_active:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            inputtedpassword = password_text
                        else:
                            password_text += event.unicode

            #clear screen
            screen.fill((255, 255, 255))

            #labels
            screen.blit(normal_font.render(usernametitle, True, "black"), (username_rect.x - 250, username_rect.y + 10))
            screen.blit(normal_font.render(passwordtitle, True, "black"), (password_rect.x - 250, password_rect.y + 10))

            #draw input boxes
            pygame.draw.rect(screen, "yellow", username_rect, 0 if username_active else 2)
            pygame.draw.rect(screen, "yellow", password_rect, 0 if password_active else 2)

            #get best fonts
            font_username = get_best_font(username_text, username_rect.w - 10, username_rect.h - 10)
            font_password = get_best_font("*" * len(password_text), password_rect.w - 10, password_rect.h - 10)

            #render text
            screen.blit(font_username.render(username_text, True, "black"), (username_rect.x + 5, username_rect.y + 5))
            screen.blit(font_password.render("*" * len(password_text), True, "black"), (password_rect.x + 5, password_rect.y + 5))

            #blinking cursor
            if cursor_visible:
                if username_active:
                    cursor_x = font_username.size(username_text)[0] + username_rect.x + 5
                    pygame.draw.line(screen, "black", (cursor_x, username_rect.y + 5), (cursor_x, username_rect.y + username_rect.h - 5), 2)
                elif password_active:
                    cursor_x = font_password.size("*" * len(password_text))[0] + password_rect.x + 5
                    pygame.draw.line(screen, "black", (cursor_x, password_rect.y + 5), (cursor_x, password_rect.y + password_rect.h - 5), 2)

            #updating whole display
            pygame.display.flip()


    if signup:
        #text boxes
        username_rect = pygame.Rect(screen.get_width() // 2 - 160, 600, 320, 50)
        password_rect = pygame.Rect(screen.get_width() // 2 - 160, 700, 320, 50)
        confpassword_rect = pygame.Rect(screen.get_width() // 2 - 160, 800, 320, 50)

        #don't activate the text boxes
        username_active = False
        password_active = False
        confpassword_active = False

        #starting text for input boxes
        username_text = ""
        password_text = ""
        confpassword_text = ""

        #cursor stuff
        cursor_visible = True
        cursor_timer = 0
        cursor_interval = 500

        #don't display error messages
        displayerror1 = False
        displayerror2 = False
        displayerror3 = False
        displayerror4 = False

        #don't breakout yet
        breakout = False

        while run:
            dt = clock.tick(60)
            cursor_timer += dt
            if cursor_timer >= cursor_interval:
                cursor_visible = not cursor_visible
                cursor_timer = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if username_rect.collidepoint(event.pos):
                        username_active = True
                        password_active = False
                        confpassword_active = False
                    elif password_rect.collidepoint(event.pos):
                        password_active = True
                        username_active = False
                        confpassword_active = False
                    elif confpassword_rect.collidepoint(event.pos):
                        confpassword_active = True
                        password_active = False
                        username_active = False
                    else:
                        confpassword_active = False
                        username_active = False
                        password_active = False

                if event.type == pygame.KEYDOWN:
                    if username_active:
                        if event.key == pygame.K_BACKSPACE:
                            username_text = username_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            displayerror1 = True
                        else:
                            username_text += event.unicode
                    elif password_active:
                        if event.key == pygame.K_BACKSPACE:
                            password_text = password_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            displayerror1 = True
                        else:
                            password_text += event.unicode
                    elif confpassword_active:
                        if event.key == pygame.K_BACKSPACE:
                            confpassword_text = confpassword_text[:-1]
                        elif event.key == pygame.K_RETURN:
                            if username_text == "" or password_text == "" or confpassword_text == "":
                                displayerror3 = True
                            else:
                                if check_username(username_text):
                                    displayerror1 = False
                                    inputtedusername = username_text
                                    inputtedpassword = password_text
                                    confpassword = confpassword_text
                                    if password_text == confpassword:
                                        breakout = True
                                        displayerror2 = False
                                    else:
                                        displayerror1 = False
                                        displayerror3 = False
                                        displayerror4 = False
                                        displayerror2 = True
                                else:
                                    displayerror1 = False
                                    displayerror3 = False
                                    displayerror2 = False
                                    displayerror4 = True
                        else:
                            confpassword_text += event.unicode

            #if breakout, do so
            if breakout:
                break

            #draw everything
            screen.fill((255, 255, 255))

            #labels
            screen.blit(normal_font.render(newusernametitle, True, "black"), (username_rect.x - 350, username_rect.y + 10))
            screen.blit(normal_font.render(newpasswordtitle, True, "black"), (password_rect.x - 350, password_rect.y + 10))
            screen.blit(normal_font.render(confpasswordtitle, True, "black"), (confpassword_rect.x - 350, confpassword_rect.y + 10))

            #draw input boxes
            pygame.draw.rect(screen, "yellow", username_rect, 0 if username_active else 2)
            pygame.draw.rect(screen, "yellow", password_rect, 0 if password_active else 2)
            pygame.draw.rect(screen, "yellow", confpassword_rect, 0 if confpassword_active else 2)

            #get best fonts
            font_username = get_best_font(username_text, username_rect.w - 10, username_rect.h - 10)
            font_password = get_best_font("*" * len(password_text), password_rect.w - 10, password_rect.h - 10)
            font_confirm_password = get_best_font("*" * len(confpassword_text), password_rect.w - 10, password_rect.h - 10)

            #render text
            screen.blit(font_username.render(username_text, True, "black"), (username_rect.x + 5, username_rect.y + 5))
            screen.blit(font_password.render("*" * len(password_text), True, "black"), (password_rect.x + 5, password_rect.y + 5))
            screen.blit(font_confirm_password.render("*" * len(confpassword_text), True, "black"), (confpassword_rect.x + 5, confpassword_rect.y + 5))

            #error messages
            if displayerror1:
                screen.blit(normal_font.render("Fill all boxes and then type enter on the confirm password box to enter credentials!", True, "red"), (850, 320))
            elif displayerror2:
                screen.blit(normal_font.render("The passwords do not match!", True, "red"), (850, 320))
            elif displayerror3:
                screen.blit(normal_font.render("One of the input fields is blank!", True, "red"), (850, 320))
            elif displayerror4:
                screen.blit(normal_font.render("Your username matches someone else's! Please choose a different one.", True, "red"), (850, 320))

            #blinking cursor
            if cursor_visible:
                if username_active:
                    cursor_x = font_username.size(username_text)[0] + username_rect.x + 5
                    pygame.draw.line(screen, "black", (cursor_x, username_rect.y + 5), (cursor_x, username_rect.y + username_rect.h - 5), 2)
                elif password_active:
                    cursor_x = font_password.size("*" * len(password_text))[0] + password_rect.x + 5
                    pygame.draw.line(screen, "black", (cursor_x, password_rect.y + 5), (cursor_x, password_rect.y + password_rect.h - 5), 2)
                elif confpassword_active:
                    cursor_x = font_confirm_password.size("*" * len(confpassword_text))[0] + confpassword_rect.x + 5
                    pygame.draw.line(screen, "black", (cursor_x, confpassword_rect.y + 5), (cursor_x, confpassword_rect.y + confpassword_rect.h - 5), 2)

            pygame.display.flip()

        if signup:
            new_user(inputtedusername)

            #generate hashing salt
            new_salt = bcrypt.gensalt()

            #encrypt password
            encryptedpassword = bcrypt.hashpw(inputtedpassword.encode("utf-8"), new_salt)

            with open("signin.txt", "a") as file:
                file.write("\n")
                file.write(f"{inputtedusername},{encryptedpassword.decode("utf-8")},{new_salt.decode("utf-8")}")

        #if the user went through the sign up space
        if signup:
            go_back_to_main = Button(500, 500, 300, 200, "Go to Game Selection", "green", "blue")
            while True:
                #clear screen
                screen.fill((255,255,255))
                
                #checking pygame events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                #diplaying that the user's account was created successfully
                success = normal_font.render("New account created successfully!", True, "black")
                success_rect = success.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
                screen.blit(success, success_rect)

                if go_back_to_main.is_clicked():
                    return inputtedusername
                
                go_back_to_main.draw(screen)
                
                #updating diplay
                pygame.display.flip()
        
sign_in()

