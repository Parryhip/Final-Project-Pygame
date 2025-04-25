#Final project: Classes

#importing pygame
import pygame

#class for buttons
class Button: 
    def __init__(self, x, y, width, height, text, color, hover_color): 
        self.rect = pygame.Rect(x, y, width, height) 
        self.text = text 
        self.color = color 
        self.hover_color = hover_color 
        self.font = pygame.font.Font(None, 36) 
 
    def draw(self, surface): 
        # Change color on hover 
        mouse_pos = pygame.mouse.get_pos() 
        if self.rect.collidepoint(mouse_pos): 
            pygame.draw.rect(surface, self.hover_color, self.rect) 
        else: 
            pygame.draw.rect(surface, self.color, self.rect) 
         
        # Render text 
        text_surface = self.font.render(self.text, True, "Black") 
        text_rect = text_surface.get_rect(center=self.rect.center) 
        surface.blit(text_surface, text_rect) 
 
    def is_clicked(self): 
        mouse_click = pygame.mouse.get_pressed() 
        if mouse_click[0] and self.rect.collidepoint(pygame.mouse.get_pos()): 
            return True 
        return False