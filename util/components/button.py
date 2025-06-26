import pygame

class Button:
    def __init__(self, x, y, w, h, text, font, text_col, bg_col, border_col, border_radius, hover_effect: bool, action=None, image=None,):
        self.original_rect = pygame.Rect(x, y, w, h)
        self.rect = self.original_rect.copy()
        self.text = text
        self.font = font
        self.text_col = text_col
        self.bg_col = bg_col
        self.border_col = border_col
        self.border_radius = border_radius
        self.action = action
        self.hover_effect = hover_effect
        self.image = image
        self.hovered = False

    def is_hovered(self, mouse_pos):
        return self.original_rect.collidepoint(mouse_pos)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def draw(self, surface):
        # hover effect
        if self.hover_effect:
            mouse_pos = pygame.mouse.get_pos()
            self.hovered = self.is_hovered(mouse_pos)
            scale = 1.1 if self.hovered else 1.0
        else:
            scale = 1.0

        new_width = int(self.original_rect.width * scale)
        new_height = int(self.original_rect.height * scale)
        new_x = self.original_rect.centerx - new_width // 2
        new_y = self.original_rect.centery - new_height // 2
        self.rect = pygame.Rect(new_x, new_y, new_width, new_height)

        if self.image:
            # image
            image_scaled = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            surface.blit(image_scaled, self.rect)
        else:
            # button
            pygame.draw.rect(surface, self.bg_col, self.rect, border_radius=self.border_radius)
            pygame.draw.rect(surface, self.border_col, self.rect, 2, border_radius=self.border_radius)

        if self.text:
            # centered text
            text_surf = self.font.render(self.text, True, self.text_col)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
