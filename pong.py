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

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def detect_collision_screen(self):
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
            print("Player Lost")  # Player loses when ball goes off the left side

        elif self.x > pygame.display.get_surface().get_width() - self.radius:  # Right of the screen
            print("AI Lost")  # AI loses when ball goes off the right side

    def detect_collision_paddle(self, paddle_player, paddle_ai):
        # Check collision with both paddles
        for paddle in [paddle_player, paddle_ai]:
            if (self.x + self.radius > paddle.x and self.x - self.radius < paddle.x + paddle.width) and \
               (self.y + self.radius > paddle.y and self.y - self.radius < paddle.y + paddle.height):

                # Adjust ball speed based on paddle movement
                paddle_speed_influence = paddle.speed * 14
                self.speed += abs(paddle.speed) * 0.05

                # Adjust ball direction based on collision position
                if self.x > paddle.x - 0.4 * paddle.width and self.x < paddle.x + paddle.width * 1.4:
                    if self.y < paddle.y + paddle.height / 9:  # Top edge of paddle
                        self.direction = -abs(self.direction)
                    elif self.y > paddle.y + paddle.height * (8 / 9):  # Bottom edge of paddle
                        self.direction = abs(self.direction)
                else:
                    self.direction = 180 - (self.direction % 360)  # Reverse horizontal direction
                    self.direction += paddle_speed_influence

                    # Prevent ball from getting stuck in near-vertical angles
                    if 85 < abs(self.direction % 360) < 95 or 265 < abs(self.direction % 360) < 275:
                        self.direction += 10 if paddle_speed_influence > 0 else -10

                # Adjust ball position to avoid overlapping with paddle
                if paddle == paddle_player:
                    self.x = paddle.x + paddle.width + self.radius
                else:
                    self.x = paddle.x - self.radius

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
    paddle_ai = Paddle(screen, sw - 50, sh // 2, paddle_width, paddle_height, generic_color, 0.004, paddle_border)

    running = True
    while running:
        dt = clock.tick(240)  # Limit frame rate to 240 FPS
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
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
        if player_movement_key[0]:
            paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2) - paddle_height * player_movement_key[1], dt)
        else:
            if pygame.mouse.get_pressed()[0]:  # Allow mouse control
                paddle_player.follow_target(mouse_y, dt)
            else:
                paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2), dt)

        # Update ball and AI paddle
        ball.update(dt)
        paddle_ai.follow_target(ball.y, dt)

        # Detect collisions
        ball.detect_collision_screen()
        ball.detect_collision_paddle(paddle_player, paddle_ai)

        # Draw everything
        screen.fill((20, 20, 25))  # Background color
        ball.draw(screen)
        paddle_player.draw(screen, dt)
        paddle_ai.draw(screen, dt)

        pygame.display.flip()  # Update the display

    pygame.quit()


main_loop()
