import pygame # import pygame
import csv # Import csv
import os # import os 
import time # time
import random # random
from leaderboard import * 

# Start the game
pygame.init()
font = pygame.font.Font(None, 36)

# Game window
W = 2560
H = 1375
win = pygame.display.set_mode((W, H))

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)

# Player info
player = {
    "x": 50,
    "y": H - 50,
    "w": 30,
    "h": 30,
    "speed": 5,
    "jump": random.randint(1, 20),
    "life": 3,
    "score": 0,
    "keys": [],
    "jump_on": False,
    "vy": 0,  # vertical velocity
    "gravity": 0.5,  # gravity value
    "max_fall_speed": 10,  # terminal velocity
    "jump_strength": -20,  # negative velocity to jump
    "hit_timer": 0,       # Countdown for red flash
    "knockback_x": 0,     # How far to knockback horizontally
    "knockback_y": 0      # Vertical knockback
}

# Game things
game = {
    "floors": [],
    "spikes": [],
    "bad": [],
    "keys": [],
    "door": pygame.Rect(W - 50, H - 100, 40, 60)
}

# Game state
state = {
    "run": True,
    "safe": 0,
    "best": 0
}

# Get best score from file
def get_best(username):
    try:
        return int(get_score(username, 3))  # platformer is 4th column (index 3)
    except:
        return 0

# Save best score to file
def save_best(username, score):
    try:
        input_score(username, 3, score)  # platformer is 4th column (index 3)
    except:
        Instrustion_text8 = font.render(f"Save score failed", True, Yellow)
        win.blit(Instrustion_text8, (10, 160))

def show_platformer_leaderboard():
    leaderboard = get_leaderboard(3)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    showing = True

    # Button setup
    button_text = small_font.render("Click Here to Return to Game Selection", True, White)
    button_rect = button_text.get_rect()
    button_rect.center = (W // 2, H - 100)

    while showing:
        win.fill(Black)

        title_text = font.render("Platformer Leaderboard (Top 10)", True, Yellow)
        win.blit(title_text, (W // 2 - title_text.get_width() // 2, 100))

        y_start = 200
        for i, (name, score) in enumerate(leaderboard[:10]):
            entry_text = small_font.render(f"{i+1}. {name} : {score}", True, White)
            win.blit(entry_text, (W // 2 - entry_text.get_width() // 2, y_start + i * 40))

        # Draw button
        pygame.draw.rect(win, Blue, button_rect.inflate(20, 10))  # button background with padding
        win.blit(button_text, button_rect)

        pygame.display.flip()
        pygame.time.wait(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    showing = False

def make_level():
    # Clear old things
    game["floors"] = []
    game["spikes"] = []
    game["bad"] = []
    game["keys"] = []

    floors = []

    # Define how many vertical layers you want (e.g., every 150 pixels)
    layer_spacing = 150
    num_layers = H // layer_spacing

    for i in range(num_layers):
        y = H - (i * layer_spacing) - 100  # move upward
        num_platforms = random.randint(2, 4)  # how many platforms per layer

        for _ in range(num_platforms):
            x = random.randint(50, W - 250)
            width = random.randint(150, 250)
            floor = pygame.Rect(x, y, width, 20)
            floors.append(floor)

            # Optional: Add spikes
            if random.random() < 0.2:
                spike_x = x + random.randint(0, width - 30)
                spike = pygame.Rect(spike_x, y + 20, 30, 30)
                game["spikes"].append(spike)

            # Optional: Add bad guys
            if random.random() < 0.3:
                bad_x = x + random.randint(10, width - 40)
                bad = pygame.Rect(bad_x, y - 40, 40, 40)
                game["bad"].append(bad)

    # Sort floors from bottom to top (for finding highest platform)
    floors.sort(key=lambda f: f.y, reverse=False)

    game["floors"] = floors

    # Add key on the highest platform
    highest = floors[0]
    game["keys"].append(pygame.Rect(highest.x + 50, highest.y - 30, 30, 30))

    # Place door near the bottom (or you can randomize it too)
    game["door"] = pygame.Rect(W - 150, H - 100, 40, 60)


def draw():
    # Draw game
    def draw_player():
        color = Red if player["hit_timer"] > 0 else Green
        pygame.draw.rect(win, color, (player["x"], player["y"], player["w"], player["h"]))
    
    # Clear screen
    win.fill(Black)
    
    # Draw floors
    for floor in game["floors"]:
        pygame.draw.rect(win, Blue, floor)
    
    # Draw spikes
    for spike in game["spikes"]:
        pygame.draw.rect(win, Red, spike)
    
    # Draw bad guys
    for bad in game["bad"]:
        pygame.draw.rect(win, Yellow, bad)
    
    # Draw keys
    for key in game["keys"]:
        pygame.draw.rect(win, White, key)
    
    # Draw door
    pygame.draw.rect(win, White, game["door"])
    
    # Draw player
    draw_player()
    
    # Show score and life
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {player['score']}", True, White)
    life_text = font.render(f"Life: {player['life']}", True, White)
    win.blit(score_text, (10, 10))
    win.blit(life_text, (10, 50))
    Instrustion_text = font.render(f"Press space to jump, Press left and right to move", True, Yellow)
    Instrustion_text2 = font.render(f"Avoid spikes and bad guys and spikes,", True, Yellow) 
    Instrustion_text3 = font.render(f"Find keys(white) to open the door(white)", True, Yellow)
    win.blit(Instrustion_text, (10, 80))
    win.blit(Instrustion_text2, (10, 120))
    win.blit(Instrustion_text3, (10, 160))

    # Update screen
    pygame.display.update()

def check_hit():
    # Check if player hits things
    # Make player box
    box = pygame.Rect(player["x"], player["y"], 
                     player["w"], player["h"])
    
    # Stop at bottom of screen
    if player["y"] > H - player["h"]:
        player["y"] = H - player["h"]
        player["vy"] = 0
        player["jump_on"] = False

    # Stop at sides
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] > W - player["w"]:
        player["x"] = W - player["w"]
    
    # Check floors
    for floor in game["floors"]:
        if box.colliderect(floor):
            # Falling onto floor
            if player["vy"] > 0 and box.bottom - player["vy"] <= floor.top:
                player["y"] = floor.top - player["h"]
                player["vy"] = 0
                player["jump_on"] = False
            # Hitting head (optional)
            elif player["vy"] < 0 and box.top - player["vy"] >= floor.bottom:
                player["y"] = floor.bottom
                player["vy"] = 0
    
    # Check keys
    for key in game["keys"][:]:
        if box.colliderect(key):
            player["keys"].append("key")
            game["keys"].remove(key)
    
    # Check door
    if player["keys"] and box.colliderect(game["door"]):
        player["score"] += 1
        player["keys"].clear()
        make_level()
    
    # Check bad things
    if time.time() > state["safe"]:
        for bad in game["bad"] + game["spikes"]:
            if box.colliderect(bad):
                player["life"] -= 1
                state["safe"] = time.time() + 3
                player["hit_timer"] = 30
                if player["x"] < bad.x:
                    player["knockback_x"] = -10  # push left
                else:
                    player["knockback_x"] = 10   # push right
                player["knockback_y"] = -5  # slight upward bump
                break
def game_over(username):
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, Red)

    while True:
        win.fill(Black)
        win.blit(text, (W // 2 - text.get_width() // 2, H // 2 - text.get_height() // 2))
        instruction = font.render("Press Enter to view leaderboard", True, Yellow)
        win.blit(instruction, (W // 2 - instruction.get_width() // 2, H // 2 + 100))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if player["score"] > state["best"]:
                    save_best(username, player["score"])
                show_platformer_leaderboard()
                state["run"] = False
                return


def platformer(username):
    # Reset game state
    state["run"] = True
    state["safe"] = 0
    state["best"] = get_best(username)

    # Reset player state
    player.update({
        "x": 50,
        "y": H - 50,
        "w": 30,
        "h": 30,
        "speed": 5,
        "jump": random.randint(1, 20),
        "life": 3,
        "score": 0,
        "keys": [],
        "jump_on": False,
        "vy": 0,
        "gravity": 0.5,
        "max_fall_speed": 10,
        "jump_strength": -20,
        "hit_timer": 0,
        "knockback_x": 0,
        "knockback_y": 0
    })

    # Make the first level
    make_level()

    # Start game clock
    clock = pygame.time.Clock()
        
    # Start the game loop
    while state["run"]:
        if player["life"] <= 0:
            # Handle game over if the player runs out of lives
            game_over(username)
            break  # End the loop after showing game over

        # Control game speed
        clock.tick(60)
        
        # Check for quit events (e.g., player clicking the X button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["run"] = False
                break  # Break out of the loop when quitting
        
        # Handle player movement (left and right)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player["x"] > 0:
            player["x"] -= player["speed"]
        if keys[pygame.K_RIGHT] and player["x"] < W - player["w"]:
            player["x"] += player["speed"]
        
        # Handle jumping
        if keys[pygame.K_SPACE] and not player["jump_on"]:
            player["vy"] = player["jump_strength"]
            player["jump_on"] = True
        
        # Apply gravity
        player["vy"] += player["gravity"]
        if player["vy"] > player["max_fall_speed"]:
            player["vy"] = player["max_fall_speed"]
        player["y"] += player["vy"]
        
        # Apply knockback if player was hit
        if player["hit_timer"] > 0:
            player["x"] += player["knockback_x"]
            player["y"] += player["knockback_y"]
            player["hit_timer"] -= 1
        else:
            player["knockback_x"] = 0
            player["knockback_y"] = 0

        # Check for collisions with environment (floors, spikes, bad guys, etc.)
        check_hit()
        
        # Draw the game elements
        draw()

    # Once state["run"] is False, the game loop ends
