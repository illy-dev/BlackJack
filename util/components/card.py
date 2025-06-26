import pygame
from constants import card_font, background_color

class Card:
    def __init__(self, x, y, w, h, card_name, text_col, image):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = card_name
        self.font = card_font
        self.text_col = text_col
        self.image = image
        self.hovered = False
        self.text_invisible = True


    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    

    def draw(self, surface):
        image_scaled = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        surface.blit(image_scaled, self.rect)

        # hover effect
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            text_surf = self.font.render(self.text, True, self.text_col)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery-100))
            surface.blit(text_surf, text_rect)
