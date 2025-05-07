# Gabriel Crozier - Pong Game

import pygame
import random
import math

# TO DO:
# - Add background (Dotted lines in middle, possible other details, check more later (gradient?))
# - Add intrustions in begining
# - Add difficulty (maybe in beggining. At least add difficulty for AI)
# - Figure out how to connect seperate files of pygame to oneanother seemlessly (exp: transitioning from game select to game with no xing out)
# - Add scoring system
# - Add player easyness (paddle collision size slighly bigger than paddle size)
# - Add 3 seconds before game starts (maybe add a countdown?)
# - Add a pause button (maybe esc key?)

# Initialize Pygame
pygame.init()

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = random.choice([random.randint(-45, 45), random.randint(135, 235)])  # Random initial direction
        self.speed = 0.75
        self.base_speed = 0.75
        self.moving = False
        self.collision_timer = 0  # Timer to prevent immediate re-collision

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def detect_collision_screen(self, score):
        # Handle collision with the top and bottom of the screen
        if self.y < self.radius:  # Top of the screen
            self.y = self.radius
            self.direction = -self.direction  # Reverse vertical direction
            self.speed += (self.base_speed - self.speed) * 0.05  # Gradual speed adjustment

        elif self.y > pygame.display.get_surface().get_height() - self.radius:  # Bottom of the screen
            self.y = pygame.display.get_surface().get_height() - self.radius
            self.direction = -self.direction
            self.speed += (self.base_speed - self.speed) * 0.05

        # Handle collision with the left and right of the screen (scoring logic)
        if self.x < self.radius:  # Left of the screen
            print(score)  # Player loses when ball goes off the left side
            return True, score

        elif self.x > pygame.display.get_surface().get_width() - self.radius:  # Right of the screen
            print(score + 1)  # AI loses when ball goes off the right side
            return True, score + 1
        
        return False, score

    def detect_collision_paddle(self, paddle_player, paddle_ai): # Fix weird bug where ball repeatedly bounces off paddle and keeps same directions (Add better print statements) (Walk through each line of code with the values to see the error)
        # Check collision with both paddles

        if round(self.collision_timer,0) > 0:
            self.collision_timer -= 1
            return

        for paddle in [paddle_player, paddle_ai]:
            if (self.x + self.radius > paddle.x and self.x - self.radius < paddle.x + paddle.width) and \
               (self.y + self.radius > paddle.y - abs(paddle.speed)*10 and self.y - self.radius < paddle.y + paddle.height + abs(paddle.speed)*10):
                self.collision_timer = 10
                print(self.direction)

                # Adjust ball speed based on paddle movement
                paddle_speed_influence = paddle.speed * 14
                self.speed += abs(paddle.speed) * 0.05

                # Adjust ball direction based on collision position
                if self.x > paddle.x and self.x < paddle.x + paddle.width:
                    if self.y < paddle.y + paddle.height * (1 / 9):
                        self.direction = -abs(self.direction)
                    elif self.y > paddle.y + paddle.height * (8 / 9):  # Bottom edge of paddle
                        self.direction = abs(self.direction)
                    else:
                        self.direction = 180 - (self.direction % 360)  # Reverse horizontal direction
                        self.direction += paddle_speed_influence
                else:
                    self.direction = 180 - (self.direction % 360)  # Reverse horizontal direction
                    self.direction += paddle_speed_influence

                    # Prevent ball from getting stuck in near-vertical angles
                    if 75 < abs(self.direction % 360) < 105 or 255 < abs(self.direction % 360) < 285:
                        self.direction += 15 if paddle_speed_influence > 0 else -15
                        self.direction += random.uniform(-5, 5)

                # Adjust ball position to avoid overlapping with paddle
                if paddle == paddle_player:
                    self.x = paddle.x + paddle.width + self.radius + 1
                else:
                    self.x = paddle.x - self.radius - 1
                print(self.direction)

    def reset_ball(self, screen):
        self.x = screen.get_width() // 2
        self.y = screen.get_height() // 2
        self.direction = random.choice([random.randint(-45, 45), random.randint(135, 235)])  # Random initial direction
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
        self.smoothness = smoothness  # Controls how smoothly the paddle follows its target
        self.scrn_mar = 25  # Screen margin
        self.scrn_hei = screen.get_height()
        self.scrn_wid = screen.get_width()
        self.speed = 0

    def draw(self, surface, dt):
        # Prevent paddle from going out of bounds (top and bottom)
        if self.y < self.scrn_mar:
            self.y += (self.scrn_mar - self.y) * 0.02 * dt
            if self.y < self.scrn_mar // 2.5:
                self.y = self.scrn_mar // 2.5

        elif self.y + self.height > self.scrn_hei - self.scrn_mar:
            self.y += ((self.scrn_hei - self.height - self.scrn_mar) - self.y) * 0.02 * dt
            if self.y + self.height > self.scrn_hei - self.scrn_mar / 2.5:
                self.y = self.scrn_hei - self.height - self.scrn_mar / 2.5

        # Draw the paddle
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), border_radius=self.border)

    def reset_paddle(self):
        self.y = self.scrn_hei // 2

    def follow_target(self, target_pos, dt):
        # Smoothly move paddle towards the target position
        self.speed = ((target_pos - (self.height // 2)) - self.y) * self.smoothness
        self.y += self.speed * dt


def main_loop():
    sw = 1000  # Screen width
    sh = 750   # Screen height
    screen = pygame.display.set_mode((sw, sh))

    clock = pygame.time.Clock()

    paddle_width = 20
    paddle_height = sh / 5
    generic_color = (255, 255, 255)  # White color for paddles and ball
    paddle_border = 7

    player_movement_key = [False, 1]  # Tracks player movement (key pressed and direction)

    pygame.display.set_caption("Pong Game")

    # Initialize ball and paddles
    ball = Circle(sw // 2, sh // 2, sh / 45, generic_color)
    paddle_player = Paddle(screen, 50, sh // 2, paddle_width, paddle_height, generic_color, 0.007, paddle_border)
    paddle_ai = Paddle(screen, sw - 50, sh // 2, paddle_width, paddle_height, generic_color, 0.007, paddle_border)

    running = True
    reset_game = True
    paused_pong = False
    scene = "pong"

    score = 0

    while running:
        dt = clock.tick(240)  # Limit frame rate to 240 FPS
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if reset_game == True:
            ball.reset_ball(screen)
            paddle_player.reset_paddle()
            paddle_ai.reset_paddle()
            reset_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if paused_pong == False:
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
        if paused_pong == False:
            if player_movement_key[0]:
                paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2) - paddle_height * player_movement_key[1], dt)
            else:
                if pygame.mouse.get_pressed()[0]:  # Allow mouse control
                    paddle_player.follow_target(mouse_y, dt)
                else:
                    paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2), dt)

        # Update ball and AI paddle
        if paused_pong == False:
            ball.update(dt)
            paddle_ai.follow_target(ball.y, dt)

            # Detect collisions
            reset_game, score = ball.detect_collision_screen(score)
            ball.detect_collision_paddle(paddle_player, paddle_ai)

        if scene == "pong":
            # Draw everything
            screen.fill((20, 20, 25))  # Background color

            # Draw the dotted line in the middle
            line_color = (220, 220, 224)  # White color for the line
            line_width = 5  # Width of each line segment
            line_height = sh//27  # Height of each line segment
            gap = sh//27  # Gap between line segments
            for y in range(0, sh, line_height + gap):
                pygame.draw.rect(screen, line_color, (sw // 2 - line_width // 2, y, line_width, line_height))

            # Draw paddles and ball
            ball.draw(screen)
            paddle_player.draw(screen, dt)
            paddle_ai.draw(screen, dt)

        pygame.display.flip()  # Update the display

    pygame.quit()


main_loop()
