import widgets
import pygame

class EmployeeManagement(widgets.Surface):
    def __init__(self, x: int, y: int, width: int, height: int, settings: widgets.Settings):
        super().__init__(x, y, width, height, settings)

    def draw(self, surface: pygame.Surface):
        surf = pygame.Surface((self.width, self.height))

        surf.fill("midnightblue")
        surface.blit(surf, (self.x, self.y))


