import pygame
from typing import overload

pygame.font.init()

def change_by_10(target: int, current: int):
    return (target - current) * 0.1

def text(text: str, font: pygame.font.FontType, color: str, background_color=None) -> pygame.Surface:
    return font.render(text, True, color, background_color)

@overload
def draw_text(surface: pygame.Surface, x: int, y: int, text_obj: pygame.Surface) -> pygame.Rect:
    ...

@overload
def draw_text(surface: pygame.Surface, x: int, y: int, text_info: list|tuple) -> pygame.Rect:
    """text_info = [text, font: pygame.font.FontType, color, background_color]"""
    ...

def draw_text(surface: pygame.Surface, x: int, y: int, stuff: list|tuple|pygame.Surface):
    if isinstance(stuff, list):
        text_surface = stuff[1].render(stuff[0], True, stuff[2], stuff[3])
        surface.blit(text_surface, (x, y))

        return text_surface.get_rect(topleft=(x, y))
    elif isinstance(stuff, pygame.Surface):
        surface.blit(stuff, (x, y))

        return stuff.get_rect(topleft=(x, y))
    else:
        raise Exception("stuff is not a text_info nor a pygame.Rect")

def draw_rotated_text(surface: pygame.Surface, x: int, y: int, text_obj: pygame.Surface, degrees: int):        
    text_obj = pygame.transform.rotate(text_obj, degrees)
    surface.blit(text_obj, (x, y))    

def draw_rectangle(surface: pygame.Surface, x: int, y: int, width: int, height: int, color: str) -> pygame.Rect:    
    if isinstance(width, str): 
        match width.lower():
            case "max":
                width = surface.get_width()

    bbox = pygame.draw.rect(surface, color, pygame.Rect(x, y, width, height))
    return bbox


class Listview:
    def __init__(self, surface: pygame.SurfaceType, rect: pygame.rect.RectType, colors: list, font, header_font):
        """colors = [selected, hovered, normal, header]"""
        self.surface = surface
        self.rect = rect
        self.colors = colors
        self.font = font
        self.header_font = header_font
        
        self.columns = []
        self.rows = []

    def set_columns(self, cols):
        self.columns = cols

    def set_values(self, vals):
        self.rows = vals

    def add_value(self, val):
        self.row.append(val)

    def draw(self):
        col_width = self.rect.width//len(self.columns)
        for count, column in enumerate(self.columns):
            header_text = text(column, self.header_font, self.colors[3])
            draw_text(self.surface, self.rect.x+(col_width*count), self.rect.y, header_text)


class BarGraph:
    DEFAULT = "#111111"

    def __init__(self, surface: pygame.Surface, x: int = 5, y: int = 5, padding: int = 5, width: int = 640, height: int = 360, 
                axis_labels: list = ["x-axis", "y-axis"], 
                axis_font: pygame.font.FontType = pygame.font.SysFont("JetbrainsMono", 14), axis_color: str = "white",
                label_font: pygame.font.FontType = pygame.font.SysFont("JetbrainsMOno", 12)):
        
        self.surface = surface
        self.x = x
        self.y = y
        self.padding = padding        
        self.width = width
        self.height = height
        self.axis_labels = axis_labels
        self.axis_font = axis_font
        self.axis_color = axis_color
        self.label_font = label_font

        self.bars = {}
        self.highlight = "yellow"
        self.other = "gray"
        
        self._calculated = False

    def add_bar(self, bar_title: str, bar_value: int, color = DEFAULT):
        self.bars[bar_title] = [bar_value, color, False]
    
    def dehighlight(self):
        for bar in self.bars:
            self.bars[bar][2] = False
            
    def highlight_bar(self, bar_name: str):
        for bar in self.bars:
            if bar_name == bar:
                self.bars[bar][2] = True
            
    def get_max_value(self):
        val = 0
        for bar in self.bars:
            val = max(val,self.bars[bar][0])
        
        return val
        
    def draw(self, rect: pygame.Rect = None):
        pass
    
                