import pygame
import json
import os

from pygame.event import EventType

pygame.init()
pygame.font.init()

class Settings:
    def __init__(self, theme, application, time=None, file=None):
        self._theme = theme
        self._application = application
        self._time = time
        self._json_file = file

        # All just _theme
        self.paddingTop = self._theme["paddingTop"]
        self.paddingRight = self._theme["paddingRight"]
        self.paddingLeft = self._theme["paddingLeft"]
        self.paddingBottom = self._theme["paddingBottom"]
        self.borderRadius = self._theme["borderRadius"]

        self.background = self._theme["background"]
        self.foreground = self._theme["foreground"]
        self.textColor = self._theme["textColor"]
        self.hoverForeground = self._theme["hoverForeground"]
        self.hoverText = self._theme["hoverText"]
        self.selectedForeground = self._theme["selectedForeground"]
        self.selectedText = self._theme["selectedText"]

        self.debugNormal = self._theme["debugNormal"]
        self.debugError = self._theme["debugError"]
        self.debugBackground = self._theme["debugBackground"]
        self.debugSuccess = self._theme["debugSuccess"]

        # All just _application
        self.width = self._application["width"]
        self.height = self._application["height"]
        self.fps = self._application["fps"]
        self.debugMode = self._application["debugMode"]
        self.currentRole = self._application["currentRole"]

    @staticmethod
    def from_json_file(json_file):
        with open(json_file) as file:
            json_dict = json.load(file)
            return Settings(**json_dict, time=os.path.getmtime(json_file), file=json_file)
        
    def __repr__(self) -> str:
        return f"<Settings {self._time}>"
        
    def check_changes(self):
        if self._time != os.path.getmtime(self._json_file):
            self = self.from_json_file(self._json_file)


class Widget:
    def __init__(self, x, y, width, height, settings):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.settings = settings

    def handle_event(self, event: pygame.event.EventType):
        pass

    def draw(self, surface: pygame.Surface):
        pass

    def collidepoint(self, x_pos, y_pos) -> bool:
        if self.x <= x_pos <= self.x+self.width:
            if self.y <= y_pos <= self.y+self.height:
                return True
            else:
                return False
        else:
            return False
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.x, self.y, self.width, self.height}>"


class TabMenu(Widget):
    def __init__(self, settings):
        self.settings = settings

        super().__init__(0, 0, 0, 0, settings)
        self.font = pygame.font.SysFont("Calibri", 15)

        self._state = 0
        self._tabs = []
        self._tab = None
        self._width = 0
        self._height = 0

    def add_tab(self, tab_name: str, tab_view: Widget):
        render = self.font.render(tab_name, True, self.settings.textColor)
        self._width += self.settings.paddingLeft + render.get_width() + self.settings.paddingRight
        self._height = max(self.settings.paddingTop+render.get_height()+self.settings.paddingBottom, self._height)
        self._tabs.append([tab_name, tab_view])

    def draw(self, surface: pygame.Surface):
        self.width = self._width
        self.height = self._height

        if self._state == 0:
            self.x = surface.get_width()//2 - self._width//2
            self.y = surface.get_height()//2 - self._height//2
        elif self._state == 1:
            self.x += (self.settings.paddingLeft - self.x) * 0.1
            self.y += (self.settings.paddingBottom - self.y) * 0.1

            if int(self.x) == int(self.settings.paddingLeft):
                self._state = 2

        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        if keys[pygame.K_1] and mods&pygame.KMOD_ALT:
            self._state = 1
            self._tab = self._tabs[0]
        elif keys[pygame.K_2] and mods&pygame.KMOD_ALT:
            self._state = 1
            self._tab = self._tabs[1]
        elif keys[pygame.K_3] and mods&pygame.KMOD_ALT:
            self._state = 1
            self._tab = self._tabs[2]

        previous = 0
        for tab in self._tabs:
            tab_render = self.font.render(tab[0], True, self.settings.textColor)

            tab_surf = pygame.Surface((self.settings.paddingLeft + tab_render.get_width() + self.settings.paddingRight, self.height))
    
            if tab_surf.get_rect(topleft=(self.x+previous, self.y)).collidepoint(*pygame.mouse.get_pos()):
                background = self.settings.hoverForeground
                if pygame.mouse.get_pressed()[0]:
                    self._state = 1
                    self._tab = tab
            else:
                background = self.settings.foreground

            if self._tab == tab:
                background = self.settings.selectedForeground

            tab_surf.fill(background)
            surface.blit(tab_surf, (self.x+previous, self.y))
            
            surface.blit(tab_render, (self.x+previous+self.settings.paddingLeft, self.y+self.settings.paddingTop))

            previous += self.settings.paddingLeft + tab_render.get_width() + self.settings.paddingRight + self.settings.paddingLeft

            if self._state == 2 and self._tab == tab:
                tab[1].x = self.x
                tab[1].y = self.y + self.height + self.settings.paddingBottom
                tab[1].width = surface.get_width() - self.settings.paddingRight - self.settings.paddingLeft
                tab[1].height = surface.get_height() - self.settings.paddingBottom - self.height - self.settings.paddingTop - self.settings.paddingBottom
                
                # surf = pygame.Surface((tab[1].width, tab[1].height))
                tab[1].draw(surface)
                # surface.blit(surf, (self.settings.paddingLeft, self.x+previous))

    def handle_event(self, event: pygame.event.Event):
        if self._state == 2:
            for tab in self._tabs:
                if self._tab == tab:
                    tab[1].handle_event(event)


class Label(Widget):
    def __init__(self, text, x, y, settings=None):
        self.text = text
        super().__init__(x, y, 0, 0, settings)

        self.set_vars()

    def set_vars(self):
        if self.settings is None:
            self.padding_top = 5
            self.padding_right = 5
            self.padding_left = 5
            self.padding_bottom = 5
            self.text_color = "black"
            self.background = "white"
            self.font = pygame.font.SysFont("Calibri", 15)

        else:
            self.padding_left = self.settings.paddingLeft
            self.padding_right = self.settings.paddingRight
            self.padding_top = self.settings.paddingTop
            self.padding_bottom = self.settings.paddingBottom
            self.text_color = self.settings.textColor
            self.background = self.settings.foreground
            self.font = pygame.font.SysFont("Calibri", 15)


        self.text_render = self.font.render(self.text, True, self.text_color)

        self.width = self.text_render.get_width() + self.padding_left + self.padding_right
        self.height = self.text_render.get_height() + self.padding_top + self.padding_bottom

    def draw(self, surface: pygame.Surface):
        surf = pygame.Surface((self.width, self.height))

        surf.fill(self.background)
        surf.blit(self.text_render, (self.padding_left, self.padding_top))

        surface.blit(surf, (self.x, self.y))

    def __repr__(self) -> str:
        return f"<Label {self.x, self.y, self.width, self.height, self.text, self.font}>"


class Button(Widget):
    def __init__(self,text, x, y, settings=None, command=None):
        self.text = text
        self.command = command
        super().__init__(x, y, 0, 0, settings)

    def calc_size(self):
        my_label = Label(self.text, self.x, self.y, self.settings)
        self.width = my_label.width
        self.height = my_label.height

    def draw(self, surface: pygame.Surface):
        my_label = Label(self.text, self.x, self.y, self.settings)
        self.width = my_label.width
        self.height = my_label.height
        my_label.draw(surface)

        if self.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            my_label.background = self.settings.hoverForeground
            my_label.text_color = self.settings.hoverText

            if pygame.mouse.get_pressed()[0]:
                if self.command is not None:
                    self.command()

        else:
            my_label.background = self.settings.foreground
            my_label.text_color = self.settings.textColor

        my_label.draw(surface)


class Window:
    def __init__(self, title, width, height, settings: Settings):

        self.title = title
        self.background = settings.background
        self.settings = settings

        self._width = width
        self._height = height
        self._window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self._funcs_in_loop = []
        self._widgets = []
        self._dt = 0

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    def get_deltatime(self):
        return self._dt
    
    def run_in_loop(self, func):
        self._funcs_in_loop.append(func)

    def add(self, widget):
        self._widgets.append(widget)

    def run(self, fps=60):
        running = True

        clock = pygame.time.Clock()
        self._dt = 0
        pygame.display.set_caption(self.title)

        while running:
            self._window.fill(self.background)

            self.settings.check_changes()

            for func in self._funcs_in_loop:
                func(self)

            for widget in self._widgets:
                widget.settings = self.settings
                widget.draw(self._window)

            self._dt = clock.tick(fps)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                for widget in self._widgets:
                    widget.handle_event(event)

