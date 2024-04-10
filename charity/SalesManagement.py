import clarity
import pygame
from datetime import datetime
import random

r = lambda: random.randint(0, 255)

class Info(clarity.Widget):
    def __init__(self, x: int, y: int, settings: clarity.Settings, title: str = "Title", 
                    info_num: str = "00", info: str = "Long Line of Information", correlated_draw_func: callable = None):
                    
        self.settings=settings

        super().__init__(x, y, 0, 0, settings)
        self.title_font = pygame.font.SysFont("Consolas", 20)
        self.information_number_font = pygame.font.SysFont("Consolas", 40)
        self.information_font = pygame.font.SysFont("Consolas", 15)

        self.title = title
        self.information_number = info_num
        self.information = info
        self.correlated_draw_func = correlated_draw_func # MUST ACCEPT SURF
        
        self.hover = False

    def draw(self, surface: pygame.Surface):
        if self.hover == True:
            bg = self.settings.foreground
            
        else:
            bg = self.settings.background
    
        title_render = self.title_font.render(self.title, True, self.settings.hoverText)
        information_num_render = self.information_number_font.render(self.information_number, True, self.settings.hoverText)
        information_render = self.information_font.render(self.information, True, self.settings.hoverText)

        padding_height = self.settings.paddingTop + self.settings.paddingBottom
        padding_width = self.settings.paddingRight + self.settings.paddingLeft
        
        self.width = max(padding_width+title_render.get_width(), padding_width+information_num_render.get_width(), padding_width+information_render.get_width())
        self.height = padding_height+title_render.get_height()+padding_height+information_num_render.get_height()+padding_height+information_render.get_height()
        
        surf = pygame.Surface((self.width, self.height))
        surf.fill(bg)

        surf.blit(title_render, ((self.width//2 - title_render.get_width()//2), self.settings.paddingTop))
        surf.blit(information_num_render, ((self.width//2 - information_num_render.get_width()//2), self.settings.paddingTop+title_render.get_height()+padding_height))
        surf.blit(information_render, ((self.width//2 - information_render.get_width()//2), padding_height+title_render.get_height()+information_num_render.get_height()+padding_height))
        
        outside_surf = pygame.Surface((self.width+(self.settings.paddingRight+self.settings.paddingLeft), (self.height+(self.settings.paddingTop+self.settings.paddingBottom))))
        outside_surf.fill(self.settings.foreground)
        surface.blit(outside_surf, (self.x, self.y))
        
        surface.blit(surf, (self.x+self.settings.paddingLeft, self.y+self.settings.paddingTop))
        
    def draw_correlated(self, surface: pygame.Surface, x: int, y: int):
        surf = pygame.Surface((surface.get_width()-x-self.settings.paddingRight, surface.get_height()-self.settings.paddingBottom-y))
        surf.fill("white")
        
        if self.correlated_draw_func is not None:
            surf.blit(self.correlated_draw_func(surf), (self.settings.paddingLeft, self.settings.paddingTop))
        
        surface.blit(surf, (x, y))


class SalesManagement(clarity.Widget):
    def __init__(self, settings):
        self.settings = settings
        
        super().__init__(0, 0, 0, 0, settings)
        
        self._generated_data = False
        self.data = []
        self.text_font = pygame.font.SysFont("Consolas", 15)
        self.generate_data()
        
        self.infos = [
            Info(self.settings.paddingLeft, self.settings.paddingTop+35, self.settings, 
                title=f"Yearly sales ({datetime.now().year})", 
                info_num=self.get_yearly_sales_total(), 
                info=f"Total sales count: {self.get_yearly_sales_count()}",
                correlated_draw_func=self.yearly_draw_func),
            
            Info(self.settings.paddingLeft, self.settings.paddingTop+35, self.settings, 
                title=f"Monthly sales ({datetime.now().strftime('%B')})", 
                info_num=self.get_monthly_sales_total(), 
                info=f"Total sales count: {self.get_monthly_sales_count()}",
                correlated_draw_func=self.monthly_draw_func),
        ]
        
        self.info_selected = None
        self.max_info_width = 0

    def generate_data(self):
        if self._generated_data == False:
            import pandas
    
            df = pandas.read_csv(r'.\\Config\\transactions.csv')
    
            # Drop column: 'Bank name'
            df = df.drop(columns=['Bank name'])
    
            # Remove all empty rows in column: 'Credit'
            df = df.dropna(subset=["Credit"])
    
            # Drop column: 'Debit'
            df = df.drop(columns=['Debit'])
    
            self.data = df.to_dict()
            self._generate_data = True
            
            # Leaves columns 'Date', 'Name', 'Account no', 'Description', 'Credit', 'Balance'
            
    def get_yearly_sales_total(self):
        self.generate_data()
        
        total = 0
        for iden in self.data["Date"]:
            if int(self.data["Date"][iden][6:]) == datetime.now().year:
                clean_amnt = float(self.data["Credit"][iden][1:].replace(",", ""))
                total += clean_amnt
        
        return "$"+str(total)
        
    def get_yearly_sales_count(self):
        self.generate_data()
        
        total = 0
        for iden in self.data["Date"]:
            if int(self.data["Date"][iden][6:]) == datetime.now().year:
                total += 1
        
        return str(total)        
        
    def yearly_draw_func(self, surface: pygame.Surface):
        self.generate_data()
        
        surf = pygame.Surface((surface.get_width()-self.settings.paddingLeft-self.settings.paddingRight, 
                                surface.get_height()-self.settings.paddingTop-self.settings.paddingBottom))
                                
        surf.fill("white")
        
        months_data = {
            "01": 0,
            "02": 0,
            "03": 0,
            "04": 0,
            "05": 0,
            "06": 0,
            "07": 0,
            "08": 0,
            "09": 0,
            "10": 0,
            "11": 0,
            "12": 0,
        }     
        months_count = {
            "01": 0,
            "02": 0,
            "03": 0,
            "04": 0,
            "05": 0,
            "06": 0,
            "07": 0,
            "08": 0,
            "09": 0,
            "10": 0,
            "11": 0,
            "12": 0,
        }      
        for iden in self.data["Date"]:
            if int(self.data["Date"][iden][6:]) == datetime.now().year:
                clean_amnt = float(self.data["Credit"][iden][1:].replace(",", ""))
                months_data[self.data["Date"][iden][:-8]] += clean_amnt
                months_count[self.data["Date"][iden][:-8]] += 1
           
        col_width = (surf.get_width()-self.settings.paddingLeft-self.settings.paddingRight-(12*(self.settings.paddingLeft+self.settings.paddingRight)))//12    
        unit_height = (surf.get_height()-(2*self.text_font.get_height())-self.settings.paddingLeft-self.settings.paddingTop)/round(max(months_data.values()), 2)
        previous = self.settings.paddingLeft
        for month in months_data:
            month_rect = pygame.Rect(self.settings.paddingLeft+previous, surf.get_height()-(unit_height*round(months_data[month])), col_width, unit_height*round(months_data[month]))
            pygame.draw.rect(surf, "red", month_rect)
            previous += col_width +  self.settings.paddingLeft + self.settings.paddingRight 
            
            render = self.text_font.render(f"{self.convert_to_name(month)} - ${months_data[month]}", True, "black")
            surf.blit(render, (month_rect.x+(month_rect.width//2 - render.get_width()//2), month_rect.y-(self.settings.paddingBottom+render.get_height())))     

            render1 = self.text_font.render(f"{months_count[month]}", True, "black")
            surf.blit(render1, (month_rect.x+(month_rect.width//2 - render1.get_width()//2), month_rect.y-(render.get_height()+self.settings.paddingBottom+render1.get_height())))     
        
        return surf
        
    def convert_to_name(self, num: str):
        num = int(num)
        
        match num:
            case 1:
                return "Jan"
            case 2:
                return "Feb"
            case 3:
                return "Mar"
            case 4:
                return "Apr"
            case 5:
                return "May"
            case 6:
                return "Jun"
            case 7:
                return "Jul"
            case 8:
                return "Aug"
            case 9:
                return "Sep"
            case 10:
                return "Oct"
            case 11:
                return "Nov"
            case 12:
                return "Dec"

    def get_monthly_sales_total(self):
        self.generate_data()
        
        total = 0
        for iden in self.data["Date"]:
            if int(self.data["Date"][iden][:-8]) == datetime.now().month:
                clean_amnt = float(self.data["Credit"][iden][1:].replace(",", ""))
                total += clean_amnt
        
        return "$"+str(total)
        
    def get_monthly_sales_count(self):
        self.generate_data()
        
        total = 0
        for iden in self.data["Date"]:
            if int(self.data["Date"][iden][:-8]) == datetime.now().month:
                total += 1
        
        return str(total)

    def monthly_draw_func(self, surface: pygame.Surface):
        self.generate_data()
        
        surf = pygame.Surface((surface.get_width()-self.settings.paddingLeft-self.settings.paddingRight, 
                                surface.get_height()-self.settings.paddingTop-self.settings.paddingBottom))
                                
        surf.fill("white")
        
        month_data = {}
        month_count = {}

        for iden in self.data["Date"]:
            if int(self.data["Date"][iden][:-8]) == datetime.now().month:
                clean_amnt = float(self.data["Credit"][iden][1:].replace(",", ""))
                month_data[self.data["Date"][iden][:-8]] = clean_amnt
                if month_count.get(self.data["Date"][iden][:-8], None) is None:
                    month_count[self.data["Date"][iden][:-8]] = 1
                else:
                    month_count[self.data["Date"][iden][:-8]] += 1                
           
        col_width = (surf.get_width()-self.settings.paddingLeft-self.settings.paddingRight-(len(month_data)*(self.settings.paddingLeft+self.settings.paddingRight)))//12    
        unit_height = (surf.get_height()-(2*self.text_font.get_height())-self.settings.paddingLeft-self.settings.paddingTop)/round(max(month_data.values()), 2)
        previous = self.settings.paddingLeft
        for day in month_data:
            day_rect = pygame.Rect(self.settings.paddingLeft+previous, surf.get_height()-(unit_height*round(month_data[day])), col_width, unit_height*round(month_data[day]))
            pygame.draw.rect(surf, "red", day_rect)
            previous += col_width +  self.settings.paddingLeft + self.settings.paddingRight 
            
            render = self.text_font.render(f"{day} - ${month_data[day]}", True, "black")
            surf.blit(render, (day_rect.x+(day_rect.width//2 - render.get_width()//2), day_rect.y-(self.settings.paddingBottom+render.get_height())))     

            render1 = self.text_font.render(f"{month_count[day]}", True, "black")
            surf.blit(render1, (day_rect.x+(day_rect.width//2 - render1.get_width()//2), day_rect.y-(render.get_height()+self.settings.paddingBottom+render1.get_height())))     
        
        return surf

    def draw(self, surface: pygame.Surface):        
        previous_height = 0
        for info in self.infos:
            info.y = (self.settings.paddingTop+30) + previous_height
            
            self.max_info_width = max(self.max_info_width, info.width)
           
            if info.x <= pygame.mouse.get_pos()[0] <= info.x + info.width:
                if info.y <= pygame.mouse.get_pos()[1] <= info.y + info.height:
                    info.hover = True
                    if pygame.mouse.get_pressed()[0]:
                        self.generate_data()
                        self.info_selected = self.infos.index(info)
                else:
                    info.hover = False
            else:
                info.hover = False        
        
            if self.info_selected == self.infos.index(info):
                info.hover = True
                x = self.settings.paddingLeft + self.max_info_width + self.settings.paddingRight + self.settings.paddingLeft + self.settings.paddingLeft
                y = self.settings.paddingTop+30
                
                info.draw_correlated(surface, x, y) # EXPANDS
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.info_selected = None 
        
            info.draw(surface)
            
            previous_height += info.height + (2*(self.settings.paddingTop + self.settings.paddingBottom))

