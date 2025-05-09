# Gabriel Crozier - Pong Game

import pygame
import random

# TO DO:
# - Add background (Dotted lines in middle, possible other details, check more later (gradient?))
# - Add ball movement and collision detection
# - Add player movement with ws or arrow keys
# - Add intrustions in begining
# - Add difficulty (maybe in beggining. At least add difficulty for AI)
# - Figure out how to connect seperate files of pygame to oneanother seemlessly (exp: transitioning from game select to game with no xing out)
# - Add AI paddle movement
# - Add scoring system





# Initialize Pygame
pygame.init()

class Circle:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def update(self):
        pass

class Paddle:
    def __init__(self, screen, x, y, width, height, color, smoothness, border=0):
        self.x = x - (width // 2)
        self.y = y - (height // 2)
        self.width = width
        self.height = height
        self.color = color
        self.border = border
        self.smoothness = smoothness  # Smoothness factor for paddle movement
        self.scrn_mar = 25  # Margin from the screen edges
        self.scrn_hei = screen.get_height()  # Screen height
        self.scrn_wid = screen.get_width() # Screen width

    def draw(self, surface, dt):
        # Ensure the paddle stays within the screen bounds
        if self.y < self.scrn_mar: # Checks if the paddle is too close to the top of the screen (Margin)
            self.y = self.y + (self.scrn_mar-self.y)*0.02*dt  # Adjust the paddle position to stay within the margin
            if self.y < self.scrn_mar//2.5:
                self.y = self.scrn_mar//2.5

        elif self.y + self.height > self.scrn_hei - self.scrn_mar:
            self.y = self.y + ((self.scrn_hei - self.height - self.scrn_mar)-self.y)*0.02*dt
            if self.y + self.height > self.scrn_hei - self.scrn_mar/2.5: # Checks if the paddle is too close to the bottom of the screen (Margin)
                self.y = self.scrn_hei - self.height - self.scrn_mar/2.5

        # Draw the paddle with rounded corners
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height),border_radius=self.border)

    # Sets y value to position of mouse, but smoooooooth
    def follow_mouse(self,mouse_y,dt):
        self.y = self.y + ((mouse_y - (self.height // 2))-self.y)*self.smoothness*dt  # Center the paddle vertically based on mouse Y position


def pong_loop():
    # Set the screen dimensions
    sw = 1000
    sh = 750
    screen = pygame.display.set_mode((sw, sh))

    # Initialize clock
    clock = pygame.time.Clock()

    # Sprite dimensions
    paddle_width = 20
    paddle_height = sh/5
    generic_color = (255, 255, 255)  # White
    paddle_border = 7

    # Set the window title
    pygame.display.set_caption("Pong Game")

    ball = Circle(sw//2, sh//2, sh/45, generic_color)  # Example circle
    paddle_player = Paddle(screen, 50, sh//2, paddle_width, paddle_height, generic_color, 0.005, paddle_border)  # Example paddle
    paddle_ai = Paddle(screen, sw-50, sh//2, paddle_width, paddle_height, generic_color, 0.005, paddle_border)  # Example AI paddle

    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the delta time
        dt = clock.tick(240)  # Limit to 240 FPS

        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Left mouse button pressed
            paddle_player.follow_mouse(mouse_y,dt)  # Update paddle position based on mouse Y position

        # Fill the screen with a color (optional)
        screen.fill((20, 20, 25))  # Black

        

        # Draw the ball and paddles
        ball.draw(screen)
        paddle_player.draw(screen,dt)
        paddle_ai.draw(screen,dt)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()

main_loop()