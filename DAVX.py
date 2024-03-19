import pygame
import DAV as dave
pygame.init()


class _InfoWidget:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.normal = "#7d8cbb"
        self.hover = "#bab2b7"
        
        self.title_font = pygame.font.SysFont("JetBrainsMono", 20, True)
        self.date_font = pygame.font.SysFont("JetBrainsMono", 12)
        self.sales_price_font = pygame.font.SysFont("JetBrainsMono", 45)
        self.sales_count_font = pygame.font.SysFont("JetBrainsMono", 14)

        self._bg = self.normal
        self._text = {}
        self._command = None

    @property
    def width(self):
       return max(self._title.get_width()+20, self._date.get_width()+20, self._sales_price.get_width()+20, self._sales_count.get_width()+20)

    @property
    def height(self):
        return 5+self._title.get_height()+5+self._date.get_height()+5+self._sales_price.get_height()+5+self._sales_count.get_height()+5

    def set_title(self, title):
        self._text["title"] = title

    def set_date(self, date):
        self._text["date"] = date

    def set_sales(self, sales_price, sales_count):
        self._text["sales_price"] = sales_price
        self._text["sales_count"] = sales_count+" sales"

    def set_command(self, command):
        self._command = command

    def start(self):
        self._title = dave.text(self._text["title"], self.title_font, "black", self._bg)
        self._date = dave.text(self._text["date"], self.date_font, "black", self._bg)
        self._sales_price = dave.text(self._text["sales_price"], self.sales_price_font, "black", self._bg)
        self._sales_count = dave.text(self._text["sales_count"], self.sales_count_font, "black", self._bg)

    def draw(self, surface):
        width = max(self._title.get_width()+20, self._date.get_width()+20, self._sales_price.get_width()+20, self._sales_count.get_width()+20)
        height = 5+self._title.get_height()+5+self._date.get_height()+5+self._sales_price.get_height()+5+self._sales_count.get_height()+5

        widget = dave.draw_rectangle(surface, self.x, self.y, width, height, self._bg)

        current_y = self.y+5
        title = dave.draw_text(surface, self.x+(width//2 - self._title.get_width()//2), current_y, [self._text["title"], self.title_font, "black", self._bg])
        current_y += title.height+5

        date = dave.draw_text(surface, self.x+(width//2 - self._date.get_width()//2), current_y, [self._text["date"], self.date_font, "black", self._bg])
        current_y += date.height+5

        sales_price = dave.draw_text(surface, self.x+(width//2 - self._sales_price.get_width()//2), current_y, [self._text["sales_price"], self.sales_price_font, "black", self._bg])
        current_y += sales_price.height+5

        sales_count = dave.draw_text(surface, self.x+(width//2 - self._sales_count.get_width()//2), current_y, [self._text["sales_count"], self.sales_count_font, "black", self._bg])

        if widget.collidepoint(*pygame.mouse.get_pos()):
            self._bg = self.hover
            if self._command is not None and pygame.mouse.get_pressed()[0]:
                self._command()
        else:
            self._bg = self.normal


class Sales:
    def __init__(self):        
        self._started = False
                
    def start(self):
        self.info = None

        ## annual
        self.yearly_info = _InfoWidget(5, 5)
        self.yearly_info.set_title("Total Sales (Yearly)")
        self.yearly_info.set_date("October 2023 - present")
        self.yearly_info.set_sales("$120000", "42")
        self.yearly_info.set_command(self.change_to_yearly)
        # self.yearly_info.set_command(self.change_to_yearly)
        self.yearly_info.start()

        ## weekly
        self.weekly_info = _InfoWidget(5, self.yearly_info.height+10)
        self.weekly_info.set_title("Total Sales (Weekly)")
        self.weekly_info.set_date("Monday - Sunday")
        self.weekly_info.set_sales("$69000", "69")
        self.weekly_info.set_command(self.change_to_weekly)
        # self.weekly_info.set_command(self.change_to_weekly)
        self.weekly_info.start()

        self.show_all_text = dave.text("Show all sales", pygame.font.SysFont("JetBrainsMono", 20), "black")
        self.show_all_bg = "#7d8cbb"

        self.go_back_text = dave.text("Go back", pygame.font.SysFont("JetBrainsMono", 20), "black")
        self.go_back_bg = "#7d8cbb"

    def change_to_yearly(self):
        self.info = "yearly"

    def change_to_weekly(self):
        self.info = "weekly"

    def draw(self, surf: pygame.surface.SurfaceType):
        if self._started is False:
            self.start()
            self._started = True
        
        self.yearly_info.draw(surf)
        self.weekly_info.draw(surf)
        
        show_all_width = max(self.yearly_info.width, self.weekly_info.width)
        show_all_widget = dave.draw_rectangle(surf, 5, self.yearly_info.height+self.weekly_info.height+15, show_all_width, self.show_all_text.get_height()+10, self.show_all_bg)
        dave.draw_text(surf, (show_all_widget.width//2) - (self.show_all_text.get_width()//2), self.yearly_info.height+self.weekly_info.height+20, self.show_all_text)

        if show_all_widget.collidepoint(*pygame.mouse.get_pos()):
            self.show_all_bg = "#bab2b7"
        else:
            self.show_all_bg = "#7d8cbb"

        go_back_width = max(self.yearly_info.width, self.weekly_info.width)
        go_back_widget = dave.draw_rectangle(surf, 5, surf.get_height()-self.go_back_text.get_height()-15, go_back_width, self.go_back_text.get_height()+10, self.go_back_bg)
        dave.draw_text(surf, (go_back_widget.width//2) - (self.go_back_text.get_width()//2), surf.get_height()-go_back_widget.height, self.go_back_text)

        if go_back_widget.collidepoint(*pygame.mouse.get_pos()):
            self.go_back_bg = "#bab2b7"
        else:
            self.go_back_bg = "#7d8cbb"      

        info_rect = pygame.Rect(10+show_all_widget.width, 5, surf.get_width()-10, surf.get_height()-10)
        pygame.draw.rect(surf, "#7d8cbb", info_rect)

        if self.info is not None:
            if self.info.lower() == "weekly":
                bargraph = dave.BarGraph(surf, axis_labels=["Weekly", "Total Sales"])
                bargraph.add_bar("Monday", 1)
                bargraph.add_bar("Tuesday", 2)
                bargraph.add_bar("Wednsday", 3)
                bargraph.add_bar("Thursday", 11)
                bargraph.add_bar("Friday", 15)
                bargraph.add_bar("Saturday", 18)
                bargraph.add_bar("Sunday", 19)
                bargraph.draw(info_rect)


class BarGraph:
    def __init__(self, surface: pygame.surface.SurfaceType, x: int = 5, y: int = 5, padding: int = 5, width: int = 640, height: int = 360, 
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


# class Sales: 
#     def __init__(self):
#         self.widget_selected = None
#         self.widget_executed = False

#         self.show_all_bg = "#7d8cbb" # bab2b7

#     def change_to_yearly(self):
#         self.widget_selected = "yearly"

#     def change_to_weekly(self):
#         self.widget_selected = "weekly"

#     def start(self):
#         ## annual
#         self.yearly_info = _InfoWidget(5, 5)
#         self.yearly_info.set_title("Total Sales (Yearly)")
#         self.yearly_info.set_date("Oct. 2023 - present")
#         self.yearly_info.set_sales("$69000", "69")
#         self.yearly_info.set_command(self.change_to_yearly)
#         self.yearly_info.start()

#         ## weekly
#         self.weekly_info = _InfoWidget(5, self.yearly_info.height+10)
#         self.weekly_info.set_title("Total Sales (Weekly)")
#         self.weekly_info.set_date("Mon. - Sun.")
#         self.weekly_info.set_sales("$2000", "2")
#         self.weekly_info.set_command(self.change_to_weekly)
#         self.weekly_info.start()

#         ## sales

#     def draw(self, surface):
#         self.yearly_info.draw(surface)
#         self.weekly_info.draw(surface)

#         font = pygame.font.SysFont("JetBrainsMono", 20)
#         self.show_all_text = dave.text("Show all sales", font, "black", self.show_all_bg)

#         show_all_width = max(self.yearly_info.width, self.weekly_info.width)
#         show_all_widget = dave.draw_rectangle(surface, 5, self.yearly_info.height+self.weekly_info.height+15, show_all_width, self.show_all_text.get_height()+10, self.show_all_bg)
#         dave.draw_text(surface, (show_all_widget.width//2) - (self.show_all_text.get_width()//2), self.yearly_info.height+self.weekly_info.height+20, self.show_all_text)

#         if self.widget_selected is None:
#             self.sales_title = dave.text("All sales", font, "black", "#7d8cbb")
#         elif self.widget_selected == "weekly":
#             self.sales_title = dave.text("Total sales (Weekly)", font, "black", "#7d8cbb")
#         elif self.widget_selected == "yearly":
#             self.sales_title = dave.text("Total sales (Yearly)", font, "black", "#7d8cbb")

#         if show_all_widget.collidepoint(*pygame.mouse.get_pos()):
#             self.show_all_bg = "#bab2b7"
#             if pygame.mouse.get_pressed()[0]:
#                 self.widget_selected = None
#         else:
#             self.show_all_bg = "#7d8cbb"

#         sales_title_widget = dave.draw_rectangle(surface, show_all_widget.x+show_all_widget.width+5, 5, surface.get_width()-show_all_widget.width-15, font.get_height()+10, "#7d8cbb")
#         dave.draw_text(surface, sales_title_widget.x+(sales_title_widget.width//2 - self.sales_title.get_width()//2), 10, self.sales_title)

#         sales_info = dave.draw_rectangle(surface, sales_title_widget.x, sales_title_widget.y+sales_title_widget.height+5, sales_title_widget.width, surface.get_height()-sales_title_widget.height-15, "#7d8cbb")
        
#         # sales listview/charts
#         if self.widget_selected is None and self.widget_executed == False:
#             pass
            
#         elif self.widget_selected == "yearly":
#             sales = {
#                 "Oct.": 3,
#                 "Nov.": 2,
#                 "Dec.": 40,
#                 "Jan.": 23,
#                 "Feb.": 4,
#             }

#             dave.draw_bar_graph(surface, sales_info, sales, ["Amount of sales", "Months"], font, ["navyblue", "red","magenta","blue","green"])
#         elif self.widget_selected == "weekly":
#             sales = {
#                 "Mon.": 3,
#                 "Tues.": 2,
#                 "Weds.": 40,
#                 "Thurs.": 23,
#                 "Fri.": 5,
#                 "Sat.": 1,
#                 "Sun.": 4,
#             }

#             dave.draw_bar_graph(surface, sales_info, sales, ["Amount of sales", "Days"], font, ["navyblue", "red","magenta","blue","green", "midnightblue", "limegreen"])

