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
    "jump_strength": -10  # negative velocity to jump
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

def make_level():
    # Clear old things
    game["floors"] = []
    game["spikes"] = []
    game["bad"] = []
    game["keys"] = []
    
    # define three base positions
    base_positions = [
        {"x": 100, "y": 400},  # left bottom
        {"x": 400, "y": 300},  # middle
        {"x": 600, "y": 400}   # right bottom
    ]
    
    # random choose a base position
    base = random.choice(base_positions)
    
    # Add floors with small random changes
    floors = []
    # first floor (starting point)
    floors.append(pygame.Rect(50, H - 100, 200, 20))
    
    # middle floor (based on base position)
    x = base["x"] + random.randint(-20, 20)  # small random
    y = base["y"] + random.randint(-20, 20)  # small random
    floors.append(pygame.Rect(x, y, 200, 20))
    
    # third floor (to key)
    x = x + random.randint(-30, 30)  # small random
    y = y - 100 + random.randint(-20, 20)  # small random
    floors.append(pygame.Rect(x, y, 200, 20))
    
    # floor to door
    floors.append(pygame.Rect(W - 150, H - 150, 200, 20))
    
    game["floors"] = floors
    
    # Add spikes near platforms
    spikes = []
    for floor in floors[1:]:  # not put spikes on the first floor
        if random.random() < 0.3:  # 30% chance to put spikes near the floor
            x = floor.x + random.randint(-20, 20)
            y = floor.y + 30
            spikes.append(pygame.Rect(x, y, 30, 30))
    game["spikes"] = spikes
    
    # Add bad guys on platforms
    bad = []
    for floor in floors[1:]:  # not put bad guys on the first floor
        if random.random() < 0.3:  # 30% probability to put bad guys on the floor
            x = floor.x + random.randint(50, 150)
            y = floor.y - 40
            bad.append(pygame.Rect(x, y, 40, 40))
    game["bad"] = bad
    
    # Add key on the highest platform
    highest_platform = min(floors, key=lambda p: p.y)
    x = highest_platform.x + random.randint(50, 150)
    y = highest_platform.y - 30
    game["keys"] = [pygame.Rect(x, y, 30, 30)]
    
    # Door position
    game["door"] = pygame.Rect(W - 50, H - 100, 40, 60)

def draw():
    # Draw game
    def draw_player():
        # Draw player
        pygame.draw.rect(win, Green, (player["x"], player["y"], 
                                    player["w"], player["h"]))
    
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
                break

def game_over(username):
    if player["score"] > state["best"]:
        save_best(username, player["score"])
    
    win.fill(Black)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, Red)
    win.blit(text, (W//2 - text.get_width()//2, H//2 - text.get_height()//2))
    pygame.display.update()
    time.sleep(3)

def platformer(username):
    # Get best score
    state["best"] = get_best(username)
    print(f"Best: {state['best']}")
    
    # Make first level
    make_level()
    
    # Start game
    clock = pygame.time.Clock()
    while state["run"]:
        if player["life"] <= 0:
            game_over(username)
            state["run"] = False

        # Control speed
        clock.tick(60)
        
        # Check quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["run"] = False
        
        # Move left and right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player["x"] > 0:
            player["x"] -= player["speed"]
        if keys[pygame.K_RIGHT] and player["x"] < W - player["w"]:
            player["x"] += player["speed"]
        
        # Jump
        if keys[pygame.K_SPACE] and not player["jump_on"]:
            player["vy"] = player["jump_strength"]
            player["jump_on"] = True
        
        # Apply gravity
        player["vy"] += player["gravity"]
        if player["vy"] > player["max_fall_speed"]:
            player["vy"] = player["max_fall_speed"]
        player["y"] += player["vy"]
        
        # Check hits
        check_hit()
        
        # Draw game
        draw()
