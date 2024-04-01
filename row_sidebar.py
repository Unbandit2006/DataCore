import widgets
import pygame


class RowSidebar:
    def __init__(self, settings: widgets.Settings) -> None:
        self.settings = settings
        self.font = pygame.font.SysFont("Calibri", 15)
        
        self.tabs = []
        self._width = 0
        self._height = 0
        self._state = 0
        self._clicked = None

    def add_tab(self, tab_name, tab_view):
        temp_surf = widgets.Surface(0, 0, None, None, self.settings)
        temp_surf.add_text(tab_name, self.font)
        
        self._width += temp_surf.width + self.settings.paddingLeft + self.settings.paddingRight
        self._height = max(temp_surf.height, self._height)
        
        self.tabs.append([temp_surf, tab_view])

    def draw(self, surface):
        init_x = surface.get_width()//2 - self._width//2
        init_y = surface.get_height()//2 - self._height//2
        width = 0   
        
        x = self.settings.paddingLeft
        y = self.settings.paddingTop + self.settings.paddingBottom + self._height
        drawalbe_width = surface.get_width() - self.settings.paddingLeft - self.settings.paddingRight
        height = surface.get_height() - y - self.settings.paddingBottom
        drawable_surf = widgets.Surface(x, y, drawalbe_width, height, self.settings)
            
        for tab in self.tabs:
            tab_surf = tab[0]
            
            if self._state == 1:
                tab_surf.x += ((self.settings.paddingLeft+width)-tab_surf.x) * 0.1
                tab_surf.y += (self.settings.paddingTop-tab_surf.y) * 0.1
            else:
                tab_surf.x = init_x + width
                tab_surf.y = init_y
            
            # collisions
            if tab_surf.collidepoint(*pygame.mouse.get_pos()):
                tab_surf.background = self.settings.hoverForeground
                
                if pygame.mouse.get_pressed()[0]:
                    drawable_surf = tab[1](drawable_surf.x, drawable_surf.y, drawable_surf.width, drawable_surf.height, self.settings)
                    self._clicked = tab
                    self._state = 1
            
            elif self._clicked != tab:
                tab_surf.background = self.settings.foreground
            
            width += tab_surf.width+self.settings.paddingLeft+self.settings.paddingRight
            
            tab_surf.draw(surface)    

        if self._state == 1:
            drawable_surf.draw(surface)

