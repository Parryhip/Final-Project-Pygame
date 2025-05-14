#Tic Tac Toe function / game
import pygame
import random
from classes import *
from leaderboard import *
import time

pygame.init()
screen = pygame.display.set_mode((2560, 1375))
clock = pygame.time.Clock()
tic_rect_1 = pygame.Rect((screen.get_width() / 2), (screen.get_height() / 2) - 240, 20, 340)
tic_rect_2 = pygame.Rect((screen.get_width() / 2) - 120, (screen.get_height() / 2) - 240, 20, 340)
tic_rect_3 = pygame.Rect((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 140, 340, 20)
tic_rect_4 = pygame.Rect((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 20, 340, 20)
tic_rect_list = [tic_rect_1, tic_rect_2, tic_rect_3, tic_rect_4]
tic_button_1 = Button((screen.get_width() / 2) - 220, (screen.get_height() / 2), 100, 100, "", "Black", "White")
tic_button_2 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2), 100, 100, "", "Black", "White")
tic_button_3 = Button((screen.get_width() / 2) + 20, (screen.get_height() / 2), 100, 100, "", "Black", "White")
tic_button_4 = Button((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 120, 100, 100, "", "Black", "White")
tic_button_5 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 120, 100, 100, "", "Black", "White")
tic_button_6 = Button((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 120, 100, 100, "", "Black", "White")
tic_button_7 = Button((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 240, 100, 100, "", "Black", "White")
tic_button_8 = Button((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 240, 100, 100, "", "Black", "White")
tic_button_9 = Button((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 240, 100, 100, "", "Black", "White")
tic_tac_X = pygame.image.load("tic_tac_toe_X.png")
tic_tac_O = pygame.image.load("tic_tac_toe_O.png")
no_button = Button((screen.get_width() / 2) + 120, (screen.get_height() / 2) - 120, 100, 100, "No", "Blue", "White")
yes_button = Button((screen.get_width() / 2) + 120, (screen.get_height() / 2) - 240, 100, 100, "Yes", "Blue", "White")
next_button = Button(screen.get_width() / 2 - 200, 1100, 300, 100, "Next", "Blue", "Red")

def tic_leaderboard(someone_has_won, tic_screen, clock):
    run = True
    tic_tac_leaderboard = get_leaderboard(2)
    font = pygame.font.SysFont(None, 24)
    win_text = font.render('You Won!', True, 'Black')
    if someone_has_won == "Player":
            #going to leaderboard loop
        while run:
            #clear screen
            tic_screen.fill("white")

            #score surfaces
            scoresurfaces = []

            #show leaderboard!
            tic_leaderboard_title = "----------TOP 10 TIC TAC SCORES----------"
            
            #surfaces
            title_surface = font.render(tic_leaderboard_title, True, (0,0,0))

            num = 1

            for score in tic_tac_leaderboard:
                scoresurfaces.append(font.render(f"{num}. {score[0]}: {score[1]}", True, (0,0,0)))
                num += 1


            for event in pygame.event.get():
                #checing if the user clicked the X button
                if event.type == pygame.QUIT:
                    run = False

            #variable for showing first score
            position = (1000, 500)

            #Showing the player they won
            screen.blit(win_text, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 400))

            #surface showing
            tic_screen.blit(title_surface, (1000, 470))
            for surface in scoresurfaces:
                tic_screen.blit(surface, position)
                position = (1000, position[1] + 30)
            
            next_button.draw(tic_screen)
            if next_button.is_clicked():
                return

            #updating displays
            pygame.display.flip()

            #setting frame_rate
            clock.tick(60)
    else:
        return

def win_checker(tic_1, tic_2, tic_3, tic_4, tic_5, tic_6, tic_7, tic_8, tic_9, tic_1_pl, tic_2_pl, tic_3_pl, tic_4_pl, tic_5_pl, tic_6_pl, tic_7_pl, tic_8_pl, tic_9_pl):
    if tic_1 == False and tic_1_pl == True and tic_2 == False and tic_2_pl == True and tic_3 == False and tic_3_pl == True:
        return "Player"
    elif tic_1 == False and tic_1_pl == True and tic_4 == False and tic_4_pl == True and tic_7 == False and tic_7_pl == True:
        return "Player"
    elif tic_4 == False and tic_4_pl == True and tic_5 == False and tic_5_pl == True and tic_6 == False and tic_6_pl == True:
        return "Player"
    elif tic_2 == False and tic_2_pl == True and tic_5 == False and tic_5_pl == True and tic_8 == False and tic_8_pl == True:
        return "Player"
    elif tic_7 == False and tic_7_pl == True and tic_8 == False and tic_8_pl == True and tic_9 == False and tic_9_pl == True:
        return "Player"
    elif tic_3 == False and tic_3_pl == True and tic_6 == False and tic_6_pl == True and tic_9 == False and tic_9_pl == True:
        return "Player"
    elif tic_1 == False and tic_1_pl == True and tic_5 == False and tic_5_pl == True and tic_9 == False and tic_9_pl == True:
        return "Player"
    elif tic_3 == False and tic_3_pl == True and tic_5 == False and tic_5_pl == True and tic_7 == False and tic_7_pl == True:
        return "Player"
    elif tic_1 == False and tic_1_pl == False and tic_2 == False and tic_2_pl == False and tic_3 == False and tic_3_pl == False:
        return "Computer"
    elif tic_1 == False and tic_1_pl == False and tic_4 == False and tic_4_pl == False and tic_7 == False and tic_7_pl == False:
        return "Computer"
    elif tic_4 == False and tic_4_pl == False and tic_5 == False and tic_5_pl == False and tic_6 == False and tic_6_pl == False:
        return "Computer"
    elif tic_2 == False and tic_2_pl == False and tic_5 == False and tic_5_pl == False and tic_8 == False and tic_8_pl == False:
        return "Computer"
    elif tic_7 == False and tic_7_pl == False and tic_8 == False and tic_8_pl == False and tic_9 == False and tic_9_pl == False:
        return "Computer"
    elif tic_3 == False and tic_3_pl == False and tic_6 == False and tic_6_pl == False and tic_9 == False and tic_9_pl == False:
        return "Computer"
    elif tic_1 == False and tic_1_pl == False and tic_5 == False and tic_5_pl == False and tic_9 == False and tic_9_pl == False:
        return "Computer"
    elif tic_3 == False and tic_3_pl == False and tic_5 == False and tic_5_pl == False and tic_7 == False and tic_7_pl == False:
        return "Computer"
    elif tic_1 == False and tic_2 == False and tic_3 == False and tic_4 == False and tic_5 == False and tic_6 == False and tic_7 == False and tic_9 == False:
        return "None"

def tic_tac_toe(username, screen, clock):
    font = pygame.font.SysFont(None, 24)
    again_text = font.render('Play Again?', True, "white")
    lose_text = font.render('You Lost', True, "White")
    tie_text = font.render('You Tied', True, 'White')
    running = True
    tic_1_active = True
    tic_2_active = True
    tic_3_active = True
    tic_4_active = True
    tic_5_active = True
    tic_6_active = True
    tic_7_active = True
    tic_8_active = True
    tic_9_active = True
    tic_1_pl_pressed = False
    tic_2_pl_pressed = False
    tic_3_pl_pressed = False
    tic_4_pl_pressed = False
    tic_5_pl_pressed = False
    tic_6_pl_pressed = False
    tic_7_pl_pressed = False
    tic_8_pl_pressed = False
    tic_9_pl_pressed = False
    player_turn = True
    someone_has_won = "None"
    
    while running:
        someone_has_won = win_checker(tic_1_active, tic_2_active, tic_3_active, tic_4_active, tic_5_active, tic_6_active, tic_7_active, tic_8_active, tic_9_active, tic_1_pl_pressed, tic_2_pl_pressed, tic_3_pl_pressed, tic_4_pl_pressed, tic_5_pl_pressed, tic_6_pl_pressed, tic_7_pl_pressed, tic_8_pl_pressed, tic_9_pl_pressed)
        if someone_has_won == "Player":
            break
        elif someone_has_won == "Computer":
            screen.fill("black")
            screen.blit(again_text, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 120))
            screen.blit(lose_text, ((screen.get_width() / 2) - 100, (screen.get_height() / 2)))
            player_turn = False
            computer_has_done_turn = True
            yes_button.draw(screen)
            if yes_button.is_clicked():
                player_turn = True
                computer_has_done_turn = False
                someone_has_won = "None"
                tic_1_active = True
                tic_2_active = True
                tic_3_active = True
                tic_4_active = True
                tic_5_active = True
                tic_6_active = True
                tic_7_active = True
                tic_8_active = True
                tic_9_active = True
                tic_1_pl_pressed = False
                tic_2_pl_pressed = False
                tic_3_pl_pressed = False
                tic_4_pl_pressed = False
                tic_5_pl_pressed = False
                tic_6_pl_pressed = False
                tic_7_pl_pressed = False
                tic_8_pl_pressed = False
                tic_9_pl_pressed = False
            no_button.draw(screen)
            if no_button.is_clicked():
                running = False
        elif someone_has_won == "None":
            screen.fill("black")
            screen.blit(again_text, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 120))
            screen.blit(tie_text, ((screen.get_width() / 2) - 100, (screen.get_height() / 2)))
            player_turn = False
            computer_has_done_turn = True
            yes_button.draw(screen)
            if yes_button.is_clicked():
                player_turn = True
                computer_has_done_turn = False
                someone_has_won = "None"
                tic_1_active = True
                tic_2_active = True
                tic_3_active = True
                tic_4_active = True
                tic_5_active = True
                tic_6_active = True
                tic_7_active = True
                tic_8_active = True
                tic_9_active = True
                tic_1_pl_pressed = False
                tic_2_pl_pressed = False
                tic_3_pl_pressed = False
                tic_4_pl_pressed = False
                tic_5_pl_pressed = False
                tic_6_pl_pressed = False
                tic_7_pl_pressed = False
                tic_8_pl_pressed = False
                tic_9_pl_pressed = False
            no_button.draw(screen)
            if no_button.is_clicked():
                running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if player_turn == True:
            screen.fill("black")
            if tic_1_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_1.draw(screen)
                if tic_button_1.is_clicked() == True:
                    tic_1_active = False
                    tic_1_pl_pressed = True
                    player_turn = False
            elif tic_1_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) - 220, (screen.get_height() / 2)))
            elif tic_1_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) - 220, (screen.get_height() / 2)))
            if tic_2_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_2.draw(screen)
                if tic_button_2.is_clicked() == True:
                    tic_2_active = False
                    tic_2_pl_pressed = True
                    player_turn = False
            elif tic_2_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) - 100, (screen.get_height() / 2)))
            elif tic_2_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) - 100, (screen.get_height() / 2)))
            if tic_3_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_3.draw(screen)
                if tic_button_3.is_clicked() == True:
                    tic_3_active = False
                    tic_3_pl_pressed = True
                    player_turn = False
            elif tic_3_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) + 20, (screen.get_height() / 2)))
            elif tic_3_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) + 20, (screen.get_height() / 2)))
            if tic_4_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_4.draw(screen)
                if tic_button_4.is_clicked() == True:
                    tic_4_active = False
                    tic_4_pl_pressed = True
                    player_turn = False
            elif tic_4_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 120))
            elif tic_4_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 120))
            if tic_5_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_5.draw(screen)
                if tic_button_5.is_clicked() == True:
                    tic_5_active = False
                    tic_5_pl_pressed = True
                    player_turn = False
            elif tic_5_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 120))
            elif tic_5_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 120))
            if tic_6_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_6.draw(screen)
                if tic_button_6.is_clicked() == True:
                    tic_6_active = False
                    tic_6_pl_pressed = True
                    player_turn = False
            elif tic_6_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 120))
            elif tic_6_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 120))
            if tic_7_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_7.draw(screen)
                if tic_button_7.is_clicked() == True:
                    tic_7_active = False
                    tic_7_pl_pressed = True
                    player_turn = False
            elif tic_7_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 240))
            elif tic_7_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) - 220, (screen.get_height() / 2) - 240))
            if tic_8_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_8.draw(screen)
                if tic_button_8.is_clicked() == True:
                    tic_8_active = False
                    tic_8_pl_pressed = True
                    player_turn = False
            elif tic_8_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 240))
            elif tic_8_pl_pressed == False:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 240))
            if tic_9_active == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                tic_button_9.draw(screen)
                if tic_button_9.is_clicked() == True:
                    tic_9_active = False
                    tic_9_pl_pressed = True
                    player_turn = False
            elif tic_9_pl_pressed == True:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_X, ((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 240))
            else:
                for rect in tic_rect_list:
                    pygame.draw.rect(screen, "White", rect)
                screen.blit(tic_tac_O, ((screen.get_width() / 2) + 20, (screen.get_height() / 2) - 240))
            pygame.display.flip()
            dt = clock.tick(60) / 1000
        elif player_turn == False:
            computer_has_done_turn = False
            while computer_has_done_turn == False:
                com_num = random.randint(1, 9)
                if tic_1_active == True or tic_2_active == True or tic_3_active == True or tic_4_active == True or tic_5_active == True or tic_6_active == True or tic_7_active == True or tic_8_active == True or tic_9_active == True:
                    if com_num == 1:
                        if tic_1_active == True:
                            tic_1_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 2:
                        if tic_2_active == True:
                            tic_2_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 3:
                        if tic_3_active == True:
                            tic_3_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 4:
                        if tic_4_active == True:
                            tic_4_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 5:
                        if tic_5_active == True:
                            tic_5_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 6:
                        if tic_6_active == True:
                            tic_6_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 7:
                        if tic_7_active == True:
                            tic_7_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 8:
                        if tic_8_active == True:
                            tic_8_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                    elif com_num == 9:
                        if tic_9_active == True:
                            tic_9_active = False
                            computer_has_done_turn = True
                            player_turn = True
                        else:
                            pass
                else:
                    computer_has_done_turn = True
                    player_turn = True
        
        pygame.display.flip()
        clock.tick(60)
    
    if someone_has_won == "Player":
        current_score = int(get_score(username, 2))
        new_score = current_score + 1
        input_score(username, 2, new_score)

    tic_leaderboard(someone_has_won, screen, clock)

    return