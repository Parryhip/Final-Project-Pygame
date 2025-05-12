import pygame # import pygame
import csv # Import csv
import os # import os 
import time # time
import random # random



# Start the game
pygame.init()

# Game window
W = 800
H = 600
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Platformer")

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
    "jump": 15,
    "life": 3,
    "score": 0,
    "keys": [],
    "jump_on": False,
    "jump_num": 15
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
def get_best():
    try:
        if not os.path.exists("game_scores.csv"):
            # Create new file with headers
            with open("game_scores.csv", "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["username", "platformer"])
            return 0

        # Read scores
        with open("game_scores.csv", "r") as f:
            r = csv.reader(f)
            next(r)  # Skip header
            scores = []
            for row in r:
                if row and len(row) > 1:  # Make sure row has enough speace
                    try:
                        scores.append(int(row[3]))  # platformer is 4th column
                    except:
                        continue
            if scores:
                return max(scores)
            return 0
    except:
        return 0

# Save best score to file
def save_best(score):
    try:
        # Read all data
        rows = []
        with open("game_scores.csv", "r") as f:
            r = csv.reader(f)
            rows = list(r)
        
        # Update score
        if len(rows) > 1:  # If file has data
            if int(rows[1][1]) < score:  # Update score if new score is higher
                rows[1][1] = str(score)  # Only update platformer score
        
        # Write back all data
        with open("game_scores.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerows(rows)  # Write all rows back
        
        print(f"New best!：{score}！")
    except:
        print("Save score failed")

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
    
    # Update screen
    pygame.display.update()

def check_hit():
    # Check if player hits things
    # Make player box
    box = pygame.Rect(player["x"], player["y"], 
                     player["w"], player["h"])
    
    # Make player fall
    if player["y"] < H - player["h"]:
        player["y"] += 5
    
    # Stop at bottom
    if player["y"] > H - player["h"]:
        player["y"] = H - player["h"]
        player["jump_on"] = False
        player["jump_num"] = 15
    
    # Stop at sides
    if player["x"] < 0:
        player["x"] = 0
    if player["x"] > W - player["w"]:
        player["x"] = W - player["w"]
    
    # Check floors
    for floor in game["floors"]:
        if (box.bottom >= floor.top and 
            box.bottom <= floor.top + 10 and
            box.right >= floor.left and 
            box.left <= floor.right):
            player["y"] = floor.top - player["h"]
            player["jump_on"] = False
            player["jump_num"] = 15
    
    # Check keys
    for key in game["keys"][:]:
        if box.colliderect(key):
            player["keys"].append("key")
            game["keys"].remove(key)
            print("You found a key! Go to door!")
    
    # Check door
    if player["keys"] and box.colliderect(game["door"]):
        player["score"] += 1
        player["keys"].clear()
        make_level()
        print("Level done!")
    
    # Check bad things
    if time.time() > state["safe"]:
        for bad in game["bad"] + game["spikes"]:
            if box.colliderect(bad):
                player["life"] -= 1
                state["safe"] = time.time() + 3
                print(f"Ouch! Life left: {player['life']}")
                break

def game_over():
    # Game over
    print(f"Game over! Score: {player['score']}")
    if player["score"] > state["best"]:
        save_best(player["score"])
        print("New best!")
    else:
        print(f"Best: {state['best']}")
    
    pygame.quit()
    exit()

def main():
    # Get best score
    state["best"] = get_best()
    print(f"Best: {state['best']}")
    
    # Make first level
    make_level()
    
    # Start game
    clock = pygame.time.Clock()
    while state["run"]:
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
        if not player["jump_on"]:
            if keys[pygame.K_SPACE]:
                player["jump_on"] = True
                player["y"] -= 15
        else:
            if player["jump_num"] >= -15:
                neg = 1 if player["jump_num"] >= 0 else -1
                player["y"] -= (player["jump_num"] ** 2) * 0.3 * neg
                player["jump_num"] -= 1
            else:
                player["jump_on"] = False
                player["jump_num"] = 15
        
        # Check hits
        check_hit()
        
        # Draw game
        draw()
        
        # Check game over
        if player["life"] <= 0:
            game_over()

if __name__ == "__main__":
    main()
