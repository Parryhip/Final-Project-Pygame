# Gabriel Crozier - Pong Game
from classes import Button
from leaderboard import get_leaderboard, get_score

import pygame
import random
import math

# TO DO:
# - Add instructions in beginning
# - Add difficulty (maybe in beginning. At least add difficulty for AI)
# - Add player easiness (paddle collision size slightly bigger than paddle size)
# - Fix bug where ball bounces constantly against paddle
# - Fix Veriticall line Bug!!! ITS STILL THERE AHFDHGFDGFDGS - IMPORTANT

# Initialize Pygame
pygame.init()


class Text:
    def __init__(self, text, font_size, color, x, y, center=True):
        self.font_size = font_size
        self.font = pygame.font.Font("fonts/bit5x5.ttf", font_size)
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.center = center

    def update(self, text, size="Default"):
        self.text = text
        if size != "Default":
            self.font_size = size
            self.font = pygame.font.Font("fonts/bit5x5.ttf", int(size))

    def draw(self, surface):
        rendered_text = self.font.render(self.text, True, self.color)
        text_rect = rendered_text.get_rect()
        if self.center:
            text_rect.center = (self.x, self.y)
        elif self.center == "Right":
            text_rect.topright = (self.x, self.y)
        else:
            text_rect.topleft = (self.x, self.y)

        # Adject text alignment
        text_rect.x += 6
        text_rect.y += 6

        # Draw the text
        surface.blit(rendered_text, text_rect)


class Button_Better(Button):
    def __init__(self, x, y, width, height, text, text_color, text_size, color, hover_color, hover_size, border=0, render_text=False):
        x -= (width // 2)
        y -= (height // 2)
        super().__init__(x, y, width, height, text, color, hover_color)
        self.hover_size_base = hover_size
        self.hover_size = 0
        self.text_size = text_size
        self.font = None
        self.text_color = text_color
        self.border = border
        self.render_text = render_text
        self.text_object = Text(text, text_size, text_color, x + width // 2 - 4, y + height // 2 - 3, center=True)


    def draw(self, surface, dt=0):

        if self.render_text:
            # Change color on hover 
            mouse_pos = pygame.mouse.get_pos() 
            if self.rect.collidepoint(mouse_pos): 
                self.hover_size += (self.hover_size_base - self.hover_size) * 0.015 * dt
                color_current = self.hover_color

            else: 
                self.hover_size += (0 - self.hover_size) * 0.01 * dt
                color_current = self.color
            
            self.rect_hover = pygame.Rect(self.rect.x - self.hover_size, self.rect.y - self.hover_size, self.rect.width + 2 * self.hover_size, self.rect.height + 2 * self.hover_size)
            # Render objects
            pygame.draw.rect(surface, color_current, (self.rect_hover), border_radius=self.border) 
            self.text_object.update(self.text, self.text_size + self.hover_size // 2)

            self.text_object.draw(surface)

    def is_clicked(self):
        if self.render_text:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
            return False
        return False


class Circle:
    def __init__(self, x, y, radius, color, sh):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = random.choice([random.randint(-45, 45), random.randint(135, 235)])
        self.base_speed = sh / 1000  # Base speed of the ball
        self.speed = self.base_speed
        self.moving = False
        self.collision_timer = 0  # Timer to prevent immediate re-collision

    def draw(self, surface):
        pygame.draw.circle(surface, (10,10,13), (self.x, self.y), self.radius + 3)
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def detect_collision_screen(self, score_player, score_ai, sw_m_half):
        # Handle collision with the top and bottom of the screen
        if self.y < self.radius:  # Top of the screen
            self.y = self.radius
            self.direction = -self.direction
            self.speed += (self.base_speed - self.speed) * 0.05

        elif self.y > pygame.display.get_surface().get_height() - self.radius:  # Bottom of the screen
            self.y = pygame.display.get_surface().get_height() - self.radius
            self.direction = -self.direction
            self.speed += (self.base_speed - self.speed) * 0.05

        # Handle collision with the left and right of the screen (scoring logic)
        if self.x < self.radius + sw_m_half:  # Left of the screen
            return True, score_player, score_ai + 1

        elif self.x > pygame.display.get_surface().get_width() - self.radius - sw_m_half:  # Right of the screen
            return True, score_player + 1, score_ai

        return False, score_player, score_ai

    def detect_collision_paddle(self, paddle_player, paddle_ai):
        # Check collision with both paddles
        if round(self.collision_timer, 0) > 0:
            self.collision_timer -= 1
            return

        for paddle in [paddle_player, paddle_ai]:
            if (self.x + self.radius > paddle.x and self.x - self.radius < paddle.x + paddle.width) and \
               (self.y + self.radius > paddle.y - abs(paddle.speed) * 15 and self.y - self.radius < paddle.y + paddle.height + abs(paddle.speed) * 15):
                self.collision_timer = 10
                # Adjust ball speed based on paddle movement
                paddle_speed_influence = paddle.speed * 14
                self.speed += abs(paddle.speed) * 0.05

                # Adjust ball direction based on collision position
                if self.x > paddle.x and self.x < paddle.x + paddle.width:
                    if self.y < paddle.y + paddle.height * (1 / 9):  # Top edge of paddle
                        self.direction = -abs(self.direction)
                    elif self.y > paddle.y + paddle.height * (8 / 9):  # Bottom edge of paddle
                        self.direction = abs(self.direction)
                    else:
                        self.direction = 180 - (self.direction % 360)
                        self.direction += paddle_speed_influence
                else:
                    self.direction = 180 - (self.direction % 360)
                    self.direction += paddle_speed_influence

                self.direction = round(self.direction,1)  # Round direction to 1 decimal place

                    # Prevent ball from getting stuck in near-vertical angles
                normalized_direction = self.direction % 360
                
                if normalized_direction > 180:
                    normalized_direction -= 360  # Normalize to range -180 to 180
                if 75 < abs(normalized_direction) < 105:  # Near 90 degrees
                    if normalized_direction > 0:
                        self.direction -= 15
                    else:
                        self.direction += 15
                elif 255 < abs(normalized_direction) < 285:  # Near 270 degrees
                    if normalized_direction > 0:
                        self.direction -= 15
                    else:
                        self.direction += 15

                # Adjust ball position to avoid overlapping with paddle
                if paddle == paddle_player:
                    self.x = paddle.x + paddle.width + self.radius + 1
                else:
                    self.x = paddle.x - self.radius - 1

    def reset_ball(self, screen):
        self.x = screen.get_width() // 2
        self.y = screen.get_height() // 2
        self.direction = random.choice([random.randint(-45, 45), random.randint(135, 235)])
        self.speed = self.base_speed

    def update(self, dt):
        # Update ball position based on direction and speed
        self.direction %= 360
        self.y += dt * self.speed * math.sin(math.radians(self.direction))
        self.x += dt * self.speed * math.cos(math.radians(self.direction))


class Paddle:
    def __init__(self, screen, x, y, width, height, color, smoothness, border=0):
        self.x = x - (width // 2)
        self.y = y - (height // 2)
        self.width = width
        self.height = height
        self.color = color
        self.border = border
        self.smoothness = smoothness
        self.scrn_mar = 25  # Screen margin
        self.scrn_hei = screen.get_height()
        self.scrn_wid = screen.get_width()
        self.speed = 0

    def draw(self, surface, dt):
        # Draw the paddle
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=self.border)

    def reset_paddle(self):
        self.y = (self.scrn_hei // 2) - (self.height // 2)  # Reset paddle to the center of the screen

    def follow_target(self, target_pos, dt):
        # Smoothly move paddle towards the target position
        self.speed = ((target_pos - (self.height // 2)) - self.y) * self.smoothness
        self.y += self.speed * dt

        # Prevent paddle from going out of bounds (top and bottom)
        if self.y < self.scrn_mar:
            self.y += (self.scrn_mar - self.y) * 0.02 * dt
            self.speed = (self.scrn_mar - self.y) * 0.02
            if self.y < self.scrn_mar // 2.5:
                self.y = self.scrn_mar // 2.5
                self.speed = 0

        elif self.y + self.height > self.scrn_hei - self.scrn_mar:
            self.y += ((self.scrn_hei - self.height - self.scrn_mar) - self.y) * 0.02 * dt
            self.speed = ((self.scrn_hei - self.height - self.scrn_mar) - self.y) * 0.02
            if self.y + self.height > self.scrn_hei - self.scrn_mar / 2.5:
                self.y = self.scrn_hei - self.height - self.scrn_mar / 2.5
                self.speed = 0


def pong_loop(username, screen, clock):
    sh = pygame.display.Info().current_h  # 30, 50 = taskbar & title bar height Screen dimensions
    sw_m = pygame.display.Info().current_w  # Screen dimensions
    #sh = 1375
    #sw_m = 2560

    sw = int(sh*(4/3)) # Aspect sw
    sw_m_half = (sw_m -sw) // 2

    paddle_width = sw // 50
    paddle_height = sh / 5
    generic_color = (255, 255, 255)  # White color for paddles and ball
    paddle_border = 7

    player_movement_key = [False, 1]  # Tracks player movement (key pressed and direction)
    pygame.display.set_caption("Pong Game")

    # Initialize ball and paddles
    ball = Circle(sw_m_half + sw // 2, sh // 2, sh / 45, generic_color, sh)
    paddle_player = Paddle(screen, sw_m_half + 50, sh // 2, paddle_width, paddle_height, generic_color, 0.007, paddle_border)
    paddle_ai = Paddle(screen, sw_m_half + sw - 50, sh // 2, paddle_width, paddle_height, generic_color, 0.006, paddle_border)

    # Initialize text
    countdown_text = Text("3", int(sh / 7.5), (255, 255, 255), sw_m_half + sw // 2, sh // 1.5, center=True)
    score_player_text = Text("0", sh // 5, (255, 255, 255), sw_m_half + sw // 2.5, sh // 7, center=True)
    score_AI_text = Text("0", sh // 5, (255, 255, 255), sw_m_half + sw - (sw // 2.5), sh // 7, center=True)

    win_lose = Text(" ", int(sh // 4), (255, 255, 255), sw_m_half + sw // 2, int(sh // 1.2), center=True)

    start_text = Text("Press Anything to Start Game", sh // 30, (255, 255, 255), sw_m_half + sw // 2, sh // 2, center=True)
    exit_button = Button_Better(sw_m_half + sw // 2, int(sh // 1.15), int((sh // 10)*3.5), sh // 9, "Exit", "White", 50, (30,30,35), (50,50,57), sh // 200, sh // 66, True)

    # Starting Variables
    running = True
    reset_game = False

    cooldown = False
    cooldown_start_time = 0
    cooldown_timer = 3

    paused_pong = True

    score_player = 0
    score_ai = 0
    score = get_score(username, 4)

    end_game = False

    start_game = True
    surface_transparent = pygame.Surface((sw_m,sh), pygame.SRCALPHA)

    # Leaderboard

    scores_got = get_leaderboard(4)
    leaderboard_text = []

    

    # Populate the leaderboard_text list with player scores from scores_got
    for i in range(len(scores_got)):
        # Calculate the maximum text length for proper alignment
        text_length = max(len(f"{scores_got[i][0]}, {scores_got[i][1]}") for i in range(len(scores_got)))
        leaderboard_text.append(
            Text(
                f"{scores_got[i][0]}, {scores_got[i][1]}",  # Format: "PlayerName, Score"
                sh // 25,  # Font size relative to screen height
                (255, 255, 255),  # White color for text
                int(sw_m_half + (sw - (text_length * sw // 45))),  # Align text based on max text length
                sh // 25,  # Y-coordinate for the first entry
                center=False  # Align text to the left
            )
        )

    # If no scores are available, display a placeholder message
    if len(scores_got) == 0:
        text_length = 14  # Length of the placeholder text
        leaderboard_text.append(
            Text(
                "NO PLAYER, NAN",  # Placeholder text
                sh // 25,  # Font size relative to screen height
                (255, 255, 255),  # White color for text
                int(sw_m_half + (sw - (text_length * sw // 45))),  # Align placeholder text
                sh // 25,  # Y-coordinate for the placeholder
                center=False  # Align text to the left
            )
        )
    
    # Define the clipping box
    clipping_box = pygame.Rect(leaderboard_text[0].x, sh // 30, text_length * sw // 45, sh // 5)  # Example box dimensions

    # Create a subsurface for the clipping area
    clipping_surface = screen.subsurface(clipping_box)

    scroll_text = Text("Scroll through leaderboard", sh // 60, (155, 155, 155), clipping_box.x + clipping_box.width - sh // 5,
                        clipping_box.y + clipping_box.height + sh // 60, center="Right")

    while running:
        dt = clock.tick(240)  # Limit frame rate to 240 FPS
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if start_game:
            paused_pong = True

        if reset_game:
            ball.reset_ball(screen)
            cooldown_start_time = pygame.time.get_ticks()
            cooldown = True
            player_movement_key[0] = False
            reset_game = False

        if cooldown:
            # Calculate the remaining cooldown time
            elapsed_time = (pygame.time.get_ticks() - cooldown_start_time) // 1000
            remaining_time = cooldown_timer - elapsed_time
            paused_pong = True
            countdown_text.update(str(int(remaining_time + 0.99)))
            paddle_ai.follow_target(sh // 2, dt)
            paddle_player.follow_target(sh // 2, dt)

            # If cooldown is over, start the game
            if remaining_time <= 0:
                cooldown = False
                paused_pong = False
                if end_game == True:
                    reset_game = True
                    start_game = True
                    score_ai = 0
                    score_player = 0
                    cooldown_timer = 3
                    win_lose.update(" ")
                    end_game = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif start_game:
                if clipping_box.collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.MOUSEWHEEL:
                        for name in leaderboard_text:
                                leaderboard_text[0].y += 1.5 * event.y
                                
                elif event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                    if exit_button.is_clicked():
                            running = False
                            break
                    if event.button == 1:
                        start_game = False
                        cooldown = True
                        cooldown_start_time = pygame.time.get_ticks()

            if not paused_pong:
                if event.type == pygame.KEYDOWN:
                    # Handle player movement keys
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        player_movement_key[0] = True
                        player_movement_key[1] = 1
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        player_movement_key[0] = True
                        player_movement_key[1] = -1
                if event.type == pygame.KEYUP:
                    # Stop player movement when keys are released
                    if event.key in [pygame.K_w, pygame.K_UP]:
                        player_movement_key[0] = False
                        player_movement_key[1] = 1
                    if event.key in [pygame.K_s, pygame.K_DOWN]:
                        player_movement_key[0] = False
                        player_movement_key[1] = -1

        # Update player paddle position
        if not paused_pong:
            if player_movement_key[0]:
                paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2) - paddle_height * 0.8 * player_movement_key[1], dt)
            else:
                if pygame.mouse.get_pressed()[0]:  # Allow mouse control
                    paddle_player.follow_target(mouse_y, dt)
                else:
                    paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2), dt)

            # Update ball and AI paddle
            ball.update(dt)

            # Checks if ball is really close to player and if so moves to center
            if ball.x < sw_m_half + sw // 4:
                paddle_ai.follow_target(sh // 2, dt)
            else:
                paddle_ai.follow_target(ball.y, dt)

            # Detect collisions
            reset_game, score_player, score_ai = ball.detect_collision_screen(score_player, score_ai, sw_m_half)
            ball.detect_collision_paddle(paddle_player, paddle_ai)

        # Draw Background
        screen.fill((20, 20, 25))  # Background color

        # Draw Everything

        # Draw the dotted line in the middle
        line_color = (220, 220, 224)  # White color for the line
        line_width = sh // 150  # Width of each line segment
        line_height = sh // 30  # Height of each line segment
        gap = sh // 31  # Gap between line segments
        for y in range(0, sh, line_height + gap):
            pygame.draw.rect(screen, line_color, (sw_m_half + (sw // 2) - (line_width // 2), y, line_width, line_height))

        # Draw the Scoreboard
        score_player_text.update(str(score_player))
        score_player_text.draw(screen)
        score_AI_text.update(str(score_ai))
        score_AI_text.draw(screen)

        if not paused_pong:
            if score_ai >= 7:
                end_game = True
                reset_game = True
                cooldown_timer = 5
                win_lose.update("Loser")

            
            elif score_player >= 7:
                end_game = True
                reset_game = True
                cooldown_timer = 5
                score = int(score) + 1
                win_lose.update("Winner")

        # Draw paddles and ball
        ball.draw(screen)
        paddle_player.draw(screen, dt)
        paddle_ai.draw(screen, dt)

        # Draw the Countdown if in cooldown phase
        if cooldown:
            countdown_text.draw(screen)

        # Display win/lose message at the end of the game
        if end_game:
            win_lose.draw(screen)

        # Handle the start game screen
        if start_game:
            # Draw a semi-transparent overlay
            pygame.draw.rect(surface_transparent, (12, 12, 15, 155), (sw_m_half, 0, sw, sh))
            screen.blit(surface_transparent, (0, 0))

            # Draw the start game text
            start_text.draw(screen)

            # Calculate the y-coordinate of the last leaderboard item
            last_item_y = leaderboard_text[0].y + (sh // 25) * len(leaderboard_text)

            # Draw leaderboard text within the clipping box
            for i, name in enumerate(leaderboard_text):
                # Update the leaderboard entry for the current user
                if name.text.split(", ")[0] == username:
                    name.update(f"{username}, {score}", sh // 25)

                # Adjust leaderboard scrolling boundaries
                if leaderboard_text[0].y > sh // 25:
                    leaderboard_text[0].y += (sh // 25 - leaderboard_text[0].y) * 0.05
                elif last_item_y < clipping_box.y + clipping_box.height:
                    leaderboard_text[0].y += (clipping_box.y + clipping_box.height - last_item_y) * 0.003

                # Render the leaderboard text
                text_surface = name.font.render(name.text, True, name.color)
                text_rect = text_surface.get_rect(topleft=(leaderboard_text[0].x, leaderboard_text[0].y + i * (sh // 25)))

                # Check if the text intersects with the clipping box
                if clipping_box.colliderect(text_rect):
                    # Adjust the text position relative to the clipping surface
                    adjusted_x = text_rect.x - clipping_box.x
                    adjusted_y = text_rect.y - clipping_box.y
                    clipping_surface.blit(text_surface, (adjusted_x, adjusted_y))

            # Draw the scroll instruction text
            scroll_text.draw(screen)

            # Draw the exit button
            exit_button.draw(screen, dt)

        # Draw black rectangles on the left and right sides of the screen
        pygame.draw.rect(screen, (12, 12, 15), (0, 0, sw_m_half, sh))  # Left side
        pygame.draw.rect(screen, (12, 12, 15), (sw_m_half + sw, 0, sw_m_half, sh))  # Right side

        pygame.display.flip()  # Update the display
    
    pygame.quit()
    return score

""""""
sh = pygame.display.Info().current_h - 50 - 35  # 30, 50 = taskbar & title bar height Screen dimensions
sw_m = pygame.display.Info().current_w  # Screen dimensions
#sh = 1375
#sw_m = 2560

screen = pygame.display.set_mode((sw_m, sh))
clock = pygame.time.Clock()

print(pong_loop("samuel", screen, clock))