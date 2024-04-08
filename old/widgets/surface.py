import pygame
from .settings import Settings

pygame.init()
pygame.font.init()


class Surface:
    def __init__(self, x: int, y: int, width: int, height: int, settings: Settings):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.settings = settings

        self.background = self.settings.foreground

        self._text_info = None
        self._image = None

    def form_text(self):
        if self._text_info is not None:
            text_render = self._text_info[1].render(self._text_info[0], True, self.settings.textColor)

        if self.width is None:
            self.width = self.settings.paddingLeft + text_render.get_width() + self.settings.paddingRight
        
        if self.height is None:
            self.height = self.settings.paddingTop + text_render.get_height() + self.settings.paddingBottom

        return text_render

    def add_text(self, string: str, font: pygame.font.FontType):
        self._text_info = [string, font]
        
        self.form_text()
        
    def collidepoint(self, x_pos, y_pos):
        self.form_text()
        if self.x <= x_pos <= self.x+self.width:
            if self.y <= y_pos <= self.y+self.height:
                return True
            else:
                return False
        else:
            return False
            
    def draw(self, surface: pygame.Surface):   
        if self._text_info:
            text_render = self.form_text()
        
        self._image = pygame.Surface((self.width, self.height))
        self._image.fill(self.background)
        if self._text_info is not None:
            self._image.blit(text_render, (self.settings.paddingTop, self.settings.paddingLeft))

        surface.blit(self._image, (self.x, self.y))
        
        