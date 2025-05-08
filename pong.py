# Gabriel Crozier - Pong Game

import pygame
import random
import math

# TO DO:
# - Add instructions in beginning
# - Add difficulty (maybe in beginning. At least add difficulty for AI)
# - Figure out how to connect separate files of pygame seamlessly (exp: transitioning from game select to game with no xing out)
# - Add player easiness (paddle collision size slightly bigger than paddle size)
# - Fix bug where ball bounces constantly against paddle
# - Fix vertical direction of ball reverter, to make game not have ball bouncing up and down constantly

# Initialize Pygame
pygame.init()


class Text:
    def __init__(self, text, font_size, color, x, y, center=True):
        self.font = pygame.font.Font("fonts/bit5x5.ttf", font_size)
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.center = center

    def update(self, text):
        self.text = text

    def draw(self, surface):
        rendered_text = self.font.render(self.text, True, self.color)
        text_rect = rendered_text.get_rect()
        if self.center:
            text_rect.center = (self.x, self.y)
        else:
            text_rect.topleft = (self.x, self.y)

        # Adject text alignment
        text_rect.x += 6
        text_rect.y += 6

        # Draw the text
        surface.blit(rendered_text, text_rect)


class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = random.choice([random.randint(-45, 45), random.randint(135, 235)])
        self.speed = 0.75
        self.base_speed = 0.75
        self.moving = False
        self.collision_timer = 0  # Timer to prevent immediate re-collision

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def detect_collision_screen(self, score_player, score_ai):
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
        if self.x < self.radius:  # Left of the screen
            return True, score_player, score_ai + 1

        elif self.x > pygame.display.get_surface().get_width() - self.radius:  # Right of the screen
            return True, score_player + 1, score_ai

        return False, score_player, score_ai

    def detect_collision_paddle(self, paddle_player, paddle_ai):
        # Check collision with both paddles
        if round(self.collision_timer, 0) > 0:
            self.collision_timer -= 1
            return

        for paddle in [paddle_player, paddle_ai]:
            if (self.x + self.radius > paddle.x and self.x - self.radius < paddle.x + paddle.width) and \
               (self.y + self.radius > paddle.y - abs(paddle.speed) * 10 and self.y - self.radius < paddle.y + paddle.height + abs(paddle.speed) * 10):
                self.collision_timer = 10
                print(f"START direct: {round(self.direction, 1):<6}, self x: {round(self.x):<3}, self y: {round(self.y):<3}, "
                      f"paddle x: {paddle.x:<3}, paddle y: {round(paddle.y):<5}, paddle speed: {round(paddle.speed, 2):<2}")

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

                    # Prevent ball from getting stuck in near-vertical angles
                    if 75 < abs(self.direction % 360) < 105 or 255 < abs(self.direction % 360) < 285:
                        self.direction += 15 if paddle_speed_influence > 0 else -15

                # Adjust ball position to avoid overlapping with paddle
                if paddle == paddle_player:
                    self.x = paddle.x + paddle.width + self.radius + 1
                else:
                    self.x = paddle.x - self.radius - 1

                print(f"END   direct: {round(self.direction, 1):<6}, self x: {round(self.x):<3}, self y: {round(self.y):<3}, "
                      f"paddle x: {paddle.x:<3}, paddle y: {round(paddle.y):<5}, paddle speed: {round(paddle.speed):<5}\n")

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


def main_loop():
    sw, sh = 1000, 750  # Screen dimensions
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

    # Initialize text
    countdown_text = Text("3", int(sh / 7.5), (255, 255, 255), sw // 2, sh // 1.5, center=True)
    score_player_text = Text("0", sh // 5, (255, 255, 255), sw // 2.5, sh // 7, center=True)
    score_AI_text = Text("0", sh // 5, (255, 255, 255), sw - (sw // 2.5), sh // 7, center=True)

    running = True
    reset_game = False
    cooldown = True
    cooldown_start_time = pygame.time.get_ticks()
    paused_pong = False
    scene = "pong"
    score_player = 0
    score_ai = 0

    while running:
        dt = clock.tick(240)  # Limit frame rate to 240 FPS
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if reset_game:
            ball.reset_ball(screen)
            cooldown_start_time = pygame.time.get_ticks()
            cooldown = True
            reset_game = False

        if cooldown:
            # Calculate the remaining cooldown time
            elapsed_time = (pygame.time.get_ticks() - cooldown_start_time) // 1000
            remaining_time = 3 - elapsed_time
            paused_pong = True
            countdown_text.update(str(int(remaining_time + 0.99)))
            paddle_ai.follow_target(sh // 2, dt)
            paddle_player.follow_target(sh // 2, dt)

            # If cooldown is over, start the game
            if remaining_time <= 0:
                cooldown = False
                paused_pong = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
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
                paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2) - paddle_height * player_movement_key[1], dt)
            else:
                if pygame.mouse.get_pressed()[0]:  # Allow mouse control
                    paddle_player.follow_target(mouse_y, dt)
                else:
                    paddle_player.follow_target(paddle_player.y + (paddle_player.height // 2), dt)

        # Update ball and AI paddle
        if not paused_pong:
            ball.update(dt)
            paddle_ai.follow_target(ball.y, dt)

            # Detect collisions
            reset_game, score_player, score_ai = ball.detect_collision_screen(score_player, score_ai)
            ball.detect_collision_paddle(paddle_player, paddle_ai)

        if scene == "pong":
            # Draw everything
            screen.fill((20, 20, 25))  # Background color

            # Draw the dotted line in the middle
            line_color = (220, 220, 224)  # White color for the line
            line_width = 5  # Width of each line segment
            line_height = sh // 30  # Height of each line segment
            gap = sh // 31  # Gap between line segments
            for y in range(0, sh, line_height + gap):
                pygame.draw.rect(screen, line_color, ((sw // 2) - (line_width // 2), y, line_width, line_height))

            # Draw the Scoreboard
            score_player_text.update(str(score_player))
            score_player_text.draw(screen)
            score_AI_text.update(str(score_ai))
            score_AI_text.draw(screen)

            # Draw paddles and ball
            ball.draw(screen)
            paddle_player.draw(screen, dt)
            paddle_ai.draw(screen, dt)

            # Draw the Countdown
            if cooldown:
                countdown_text.draw(screen)

        pygame.display.flip()  # Update the display

    pygame.quit()


main_loop()
