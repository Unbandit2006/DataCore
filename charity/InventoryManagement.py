import clarity
import pygame
import json
import os
import webbrowser

class InventoryItem:
    def __init__(self, information):
        self.name = information["itemName"]
        self.cost = information["cost"]
        self.upc = information["upc"]
        self.buy_link = information["buyLink"]
        self.image_path = information["image"]
        self.image_data = information["cropData"]

        self.editing = False

    def __eq__(self, other) -> bool:
        if not isinstance(other, InventoryItem):
            return NotImplemented
        
        return self.name == other.name and self.cost == other.cost and self.upc == other.upc and self.buy_link == other.buy_link and self.image_data == other.image_data and self.image_path == other.image_path

    def __repr__(self) -> str:
        return f"<Item '{self.name}' ${str(self.cost)} {self.upc} {self.buy_link} {self.image_path}>"
    
    def __json__(self):
        return {
            "itemName": self.name,
            "cost": self.cost,
            "upc": self.upc,
            "buyLink": self.buy_link,
            "image": self.image_path,
            "cropData": self.image_data
        }


class InventoryGraphic(clarity.Widget):
    def __init__(self, x, y, data: InventoryItem, settings: clarity.Settings, font: pygame.font.FontType = pygame.font.SysFont("Consolas", 15)):
        self.x = x
        self.y = y
        self.data = data
        self.settings = settings
        self.font = font

        self.image = None

        self.calculate_size()

        super().__init__(self.x, self.y, self.width, self.height, self.settings)

    def calculate_size(self):
        self.width = 0
        self.height = 0

        self.width += self.settings.paddingLeft + 100 + self.settings.paddingRight
        self.height += self.settings.paddingTop + 100 + self.settings.paddingBottom

        text_height = self.settings.paddingTop + self.settings.paddingBottom
        text_width = self.settings.paddingLeft + self.settings.paddingLeft

        name_render_height = text_height +self.font.render("Name: "+self.data.name, True, self.settings.textColor).get_height()
        name_render_width = text_width +self.font.render("Name: "+self.data.name, True, self.settings.textColor).get_width()
        text_width = max(text_width, name_render_width)
        text_height += name_render_height

        cost_render_height = self.settings.paddingTop + self.settings.paddingBottom + self.font.render("Cost: $"+str(self.data.cost), True, self.settings.textColor).get_height()
        cost_render_width = self.settings.paddingLeft + self.settings.paddingRight + self.font.render("Cost: $"+str(self.data.cost), True, self.settings.textColor).get_width()
        text_width = max(text_width, cost_render_width)
        text_height += cost_render_height

        upc_render_height = self.settings.paddingTop + self.settings.paddingBottom + self.font.render("UPC: "+str(self.data.upc), True, self.settings.textColor).get_height()
        upc_render_width = self.settings.paddingLeft + self.settings.paddingRight + self.font.render("UPC: "+str(self.data.upc), True, self.settings.textColor).get_width()
        text_width = max(text_width, upc_render_width)
        text_height += upc_render_height

        link_render_height = self.settings.paddingTop + self.settings.paddingBottom + self.font.render("Link: "+self.data.buy_link, True, self.settings.textColor).get_height()
        link_render_width = self.settings.paddingLeft + self.settings.paddingRight + self.font.render("Link: "+self.data.buy_link, True, self.settings.textColor).get_width()
        text_width = max(text_width, link_render_width)
        text_height += link_render_height

        edit_text = self.font.render("Edit", True, "black")
        edit_rect = edit_text.get_rect(topleft=((self.width-self.settings.paddingRight-(edit_text.get_width()+self.settings.paddingLeft+self.settings.paddingRight)), 
                                                self.height-self.settings.paddingBottom-(edit_text.get_height()+self.settings.paddingTop+self.settings.paddingBottom)),
                                                width = self.settings.paddingLeft + edit_text.get_width() + self.settings.paddingRight,
                                                height = self.settings.paddingTop + edit_text.get_height() + self.settings.paddingBottom
                                                )

        self.width += max(self.width, text_width) + edit_rect.width + self.settings.paddingLeft + self.settings.paddingRight
        self.height = max(self.height, text_height) + edit_rect.height + self.settings.paddingBottom + self.settings.paddingTop

    def resize_image(self):
        self.image = pygame.image.load(self.data.image_path)
        self.image = self.image.subsurface(self.data.image_data[0], self.data.image_data[1], self.data.image_data[2], self.data.image_data[3])
        self.image = pygame.transform.smoothscale(self.image, (100, 100))

    def draw(self, surface: pygame.Surface, widget_parent: clarity.Widget):
        item_surface = pygame.Surface((self.width, self.height))
        item_surface.fill(self.settings.background)

        edit_color = self.settings.foreground
        edit_text_color = self.settings.textColor

        if self.data.editing:
            edit_color = self.settings.hoverForeground
            edit_text_color = self.settings.hoverText

        if self.image is None:
            self.resize_image()
        item_surface.blit(self.image, (self.settings.paddingLeft, self.settings.paddingTop))

        name_render = self.font.render("Name: "+self.data.name, True, self.settings.hoverText)
        cost_render = self.font.render("Cost: $"+str(self.data.cost), True, self.settings.hoverText)
        upc_render = self.font.render("UPC: "+str(self.data.upc), True, self.settings.hoverText)
        link_render = self.font.render("Link: ", True, self.settings.hoverText)
        self.font.set_underline(True)
        link_2_render = self.font.render(self.data.buy_link, True, "cyan")
        self.font.set_underline(False)

        y = self.settings.paddingTop
        item_surface.blit(name_render, (self.settings.paddingLeft+100+self.settings.paddingRight, self.settings.paddingTop))
        y += name_render.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        item_surface.blit(cost_render, (self.settings.paddingLeft+100+self.settings.paddingRight, y))
        y += cost_render.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        item_surface.blit(upc_render, (self.settings.paddingLeft+100+self.settings.paddingRight, y))
        y += upc_render.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        item_surface.blit(link_render, (self.settings.paddingLeft+100+self.settings.paddingRight, y))
        item_surface.blit(link_2_render, (self.settings.paddingLeft+100+self.settings.paddingRight+link_render.get_width(), y))

        edit_text = self.font.render("Edit", True, edit_text_color)
        edit_rect = edit_text.get_rect(topleft=((self.width-self.settings.paddingRight-(edit_text.get_width()+self.settings.paddingLeft+self.settings.paddingRight)), 
                                                self.height-self.settings.paddingBottom-(edit_text.get_height()+self.settings.paddingTop+self.settings.paddingBottom)),
                                                width = self.settings.paddingLeft + edit_text.get_width() + self.settings.paddingRight,
                                                height = self.settings.paddingTop + edit_text.get_height() + self.settings.paddingBottom
                                                )

        # print(edit_rect.x <= pygame.mouse.get_pos()[0]+widget_parent.x+self.settings.paddingLeft <= edit_rect.x+edit_rect.width)
        # print(edit_rect.y <= pygame.mouse.get_pos()[1]-35 <= edit_rect.y+edit_rect.height)
        x_offset = widget_parent.x+self.settings.paddingLeft+self.x
        y_offset = 35+self.y

        if self.settings.paddingLeft+100+self.settings.paddingRight+x_offset <= pygame.mouse.get_pos()[0] <= self.settings.paddingLeft+100+self.settings.paddingRight+link_render.get_width() + x_offset + link_2_render.get_width():
            if y+y_offset <= pygame.mouse.get_pos()[1] <= y+link_2_render.get_height()+y_offset:
                if pygame.mouse.get_pressed()[0]:
                    webbrowser.open(self.data.buy_link)

        if edit_rect.x + x_offset <= pygame.mouse.get_pos()[0] <= edit_rect.x+edit_rect.width + x_offset:
            if edit_rect.y+y_offset <= pygame.mouse.get_pos()[1] <= edit_rect.y+edit_rect.height+y_offset:
                edit_color = self.settings.hoverForeground
                edit_text_color = self.settings.hoverText

                if pygame.mouse.get_pressed()[0]:
                    self.data.editing = True

        edit_text = self.font.render("Edit", True, edit_text_color)
        pygame.draw.rect(item_surface, edit_color, edit_rect)
        item_surface.blit(edit_text, (edit_rect.x+self.settings.paddingLeft, edit_rect.y+self.settings.paddingRight))

        surface.blit(item_surface, (self.x, self.y))


class InventoryManagement(clarity.Widget):
    def __init__(self, settings: clarity.Settings):
        super().__init__(0, 0, 0, 0, settings)

        self.items = []
        self.item_generated_time = None
        self.item_index = None
        self.image = None
        self.currently_selected = None
        self.font = pygame.font.SysFont("Consolas", 15)
        self.event = None

    def generate_items(self):
        with open("Config\\items.json") as file:
            items = json.load(file)["items"]

            for item in items:
                self.items.append(InventoryItem(item))
    
    def get_from_file_items(self):
        values = []
        with open("Config\\items.json") as file:
            items = json.load(file)["items"]

            for item in items:
                values.append(InventoryItem(item))

        return values

    def resize_image(self, item_index: int):
        self.image = pygame.image.load(self.items[item_index].image_path)
        self.image = self.image.subsurface(self.items[item_index].image_data[0], self.items[item_index].image_data[1], self.items[item_index].image_data[2], self.items[item_index].image_data[3])
        self.image = pygame.transform.smoothscale(self.image, (100, 100))

    def draw_edit_window(self, surface: pygame.Surface, item_index: int):
        width = 0
        height = 0

        width += self.settings.paddingLeft + 100 + self.settings.paddingRight
        height += self.settings.paddingTop + 100 + self.settings.paddingBottom

        text_height = self.settings.paddingTop + self.settings.paddingBottom
        text_width = self.settings.paddingLeft + self.settings.paddingLeft

        name_render_height = text_height + self.font.render("Name: "+self.items[item_index].name, True, self.settings.textColor).get_height()
        name_render_width = text_width + self.font.render("Name: "+self.items[item_index].name, True, self.settings.textColor).get_width()
        text_width = max(text_width, name_render_width)
        text_height += name_render_height

        cost_render_height = 2*(self.settings.paddingTop + self.settings.paddingBottom) + self.font.render("Cost: $"+str(+self.items[item_index].cost), True, self.settings.textColor).get_height()
        cost_render_width = 2*(self.settings.paddingLeft + self.settings.paddingRight) + self.font.render("Cost: $"+str(self.items[item_index].cost), True, self.settings.textColor).get_width()
        text_width = max(text_width, cost_render_width)
        text_height += cost_render_height

        upc_render_height = 2*(self.settings.paddingTop + self.settings.paddingBottom) + self.font.render("UPC: "+str(self.items[item_index].upc), True, self.settings.textColor).get_height()
        upc_render_width = 2*(self.settings.paddingLeft + self.settings.paddingRight) + self.font.render("UPC: "+str(self.items[item_index].upc), True, self.settings.textColor).get_width()
        text_width = max(text_width, upc_render_width)
        text_height += upc_render_height

        link_render_height = 2*(self.settings.paddingTop + self.settings.paddingBottom) + self.font.render("Link: "+self.items[item_index].buy_link, True, self.settings.textColor).get_height()
        link_render_width = 2*(self.settings.paddingLeft + self.settings.paddingRight) + self.font.render("Link: "+self.items[item_index].buy_link, True, self.settings.textColor).get_width()
        text_width = max(text_width, link_render_width)
        text_height += link_render_height

        width += max(width, text_width)
        height = max(height, text_height) + self.font.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        if self.image is None:
            self.resize_image(item_index)

        surf = pygame.Surface((width, height))
        pos = ((self.width//2 - width//2), (self.height//2 - height//2))
        surf.fill(self.settings.background)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.currently_selected = None
            self.items[item_index].editing = False

        y = self.settings.paddingTop

        name_label_render = self.font.render("Name: ", True, self.settings.hoverText)
        surf.blit(name_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        name_render = self.font.render("Name: "+self.items[item_index].name, True, self.settings.textColor)
        act_name = self.font.render(self.items[item_index].name, True, self.settings.textColor)
        name_rect = name_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+name_label_render.get_width(), y))
        name_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - name_label_render.get_width()
        
        if name_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= name_rect.x+name_rect.width+pos[0] and name_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= name_rect.y+name_rect.height+pos[1]+35:
            name_bg = self.settings.hoverForeground
            name_text_color = self.settings.hoverText

            if pygame.mouse.get_pressed()[0]:
                self.currently_selected = "name"

        else:
            name_bg = self.settings.foreground
            name_text_color = self.settings.textColor

        if self.currently_selected == "name":
            name_bg = self.settings.selectedForeground
            name_text_color = self.settings.selectedText

            if keys[pygame.K_BACKSPACE]:
                self.items[item_index].name = self.items[item_index].name[:-1]
            elif keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                self.items[item_index].editing = False
                self.currently_selected = None
            elif keys[pygame.K_SPACE]:
                self.items[item_index].name += " "
            elif keys[pygame.K_TAB]:
                self.currently_selected = None
        
        act_name = self.font.render(self.items[item_index].name, True, name_text_color)
        pygame.draw.rect(surf, name_bg, name_rect)
        surf.blit(act_name, (name_rect.x, name_rect.y))

        y += int(name_rect.height) + self.settings.paddingBottom + self.settings.paddingTop

        cost_label_render = self.font.render("Cost: $", True, self.settings.hoverText)
        surf.blit(cost_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        cost_render = self.font.render("Cost: $"+str(self.items[item_index].cost), True, self.settings.textColor)
        act_cost = self.font.render(str(self.items[item_index].cost), True, self.settings.textColor)
        cost_rect = cost_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+cost_label_render.get_width(), y))
        cost_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - cost_label_render.get_width()

        if cost_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= cost_rect.x+cost_rect.width+pos[0] and cost_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= cost_rect.y+cost_rect.height+pos[1]+35:
            cost_bg = self.settings.hoverForeground
            cost_text_color = self.settings.hoverText

            if pygame.mouse.get_pressed()[0]:
                self.currently_selected = "cost"

        else:
            cost_bg = self.settings.foreground
            cost_text_color = self.settings.textColor

        if self.currently_selected == "cost":
            cost_bg = self.settings.selectedForeground
            cost_text_color = self.settings.selectedText

            if keys[pygame.K_BACKSPACE]:
                self.items[item_index].cost = int(str(self.items[item_index].cost)[:-1])
            elif keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                self.items[item_index].editing = False
                self.currently_selected = None
            elif keys[pygame.K_TAB]:
                self.currently_selected = None

        act_cost = self.font.render(str(self.items[item_index].cost), True, cost_text_color)
        pygame.draw.rect(surf, cost_bg, cost_rect)
        surf.blit(act_cost, (cost_rect.x, cost_rect.y))

        y += int(cost_rect.height) + self.settings.paddingBottom + self.settings.paddingTop

        upc_label_render = self.font.render("UPC: ", True, self.settings.hoverText)
        surf.blit(upc_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        upc_render = self.font.render("UPC: "+str(self.items[item_index].upc), True, self.settings.textColor)
        act_upc = self.font.render(str(self.items[item_index].upc), True, self.settings.textColor)
        upc_rect = upc_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+upc_label_render.get_width(), y))
        upc_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - upc_label_render.get_width()

        if upc_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= upc_rect.x+upc_rect.width+pos[0] and upc_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= upc_rect.y+upc_rect.height+pos[1]+35:
            upc_bg = self.settings.hoverForeground
            upc_text_color = self.settings.hoverText

            if pygame.mouse.get_pressed()[0]:
                self.currently_selected = "upc"

        else:
            upc_bg = self.settings.foreground
            upc_text_color = self.settings.textColor

        if self.currently_selected == "upc":
            upc_bg = self.settings.selectedForeground
            upc_text_color = self.settings.selectedText

            if keys[pygame.K_BACKSPACE]:
                self.items[item_index].upc = int(str(self.items[item_index].upc)[:-1])
            elif keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                self.items[item_index].editing = False
                self.currently_selected = None
            elif keys[pygame.K_TAB]:
                self.currently_selected = None

        act_upc = self.font.render(str(self.items[item_index].upc), True, upc_text_color)
        pygame.draw.rect(surf, upc_bg, upc_rect)
        surf.blit(act_upc, (upc_rect.x, upc_rect.y))

        y += int(upc_rect.height) + self.settings.paddingBottom + self.settings.paddingTop

        link_label_render = self.font.render("Link: ", True, self.settings.hoverText)
        surf.blit(link_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        link_render = self.font.render("Role: "+str(self.items[item_index].buy_link), True, self.settings.textColor)
        act_link = self.font.render(str(self.items[item_index].buy_link), True, self.settings.textColor)
        link_rect = link_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+link_label_render.get_width(), y))
        link_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - link_label_render.get_width()
        
        if link_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= link_rect.x+link_rect.width+pos[0] and link_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= link_rect.y+link_rect.height+pos[1]+35:
            link_bg = self.settings.hoverForeground
            link_text_color = self.settings.hoverText

            if pygame.mouse.get_pressed()[0]:
                self.currently_selected = "link"

        else:
            link_bg = self.settings.foreground
            link_text_color = self.settings.textColor        

        if self.currently_selected == "link":
            link_bg = self.settings.selectedForeground
            link_text_color = self.settings.selectedText

            if keys[pygame.K_BACKSPACE]:
                self.items[item_index].buy_link = self.items[item_index].role[:-1]
            elif keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                self.items[item_index].editing = False
                self.currently_selected = None
            elif keys[pygame.K_SPACE]:
                self.items[item_index].buy_link += " "
            elif keys[pygame.K_TAB]:
                self.currently_selected = None

        act_link = self.font.render(str(self.items[item_index].buy_link), True, link_text_color)
        pygame.draw.rect(surf, link_bg, link_rect)
        surf.blit(act_link, (link_rect.x, link_rect.y))

        y_area = surf.get_height() - self.settings.paddingBottom - self.settings.paddingTop - 100
        x_area = surf.get_width() - self.settings.paddingRight - self.settings.paddingLeft

        esc_render = self.font.render("Press *Esc* to exit", True, self.settings.hoverText)
        surf.blit(esc_render, (self.settings.paddingLeft+(x_area//2 - esc_render.get_width()//2), self.settings.paddingTop+self.settings.paddingBottom+100))

        tab_render = self.font.render("Press *Tab* to deselect", True, self.settings.hoverText)
        surf.blit(tab_render, (self.settings.paddingLeft+(x_area//2 - esc_render.get_width()//2), self.settings.paddingTop+self.settings.paddingTop+self.settings.paddingBottom+100+esc_render.get_height()+self.settings.paddingTop))

        surf.blit(self.image, (self.settings.paddingLeft, self.settings.paddingTop))

        # if pos[0] + self.settings.paddingLeft <= pygame.mouse.get_pos()[0] <= pos[0] + 100+self.settings.paddingLeft:
        #     if pos[1] + self.settings.paddingTop+35 <= pygame.mouse.get_pos()[1] <= pos[1]+35+100+self.settings.paddingTop:
        #         image_overlay = pygame.Surface((100, 100), pygame.SRCALPHA)
        #         image_overlay.fill((0, 0, 0, 100))
        #         surf.blit(image_overlay, (self.settings.paddingLeft, self.settings.paddingTop))

        #         if pygame.mouse.get_pressed()[0]:
        #             self.currently_selected = "image"

        # if self.currently_selected == "image":
        #     image_overlay = pygame.Surface((100, 100), pygame.SRCALPHA)
        #     image_overlay.fill((0, 0, 0, 100))
        #     surf.blit(image_overlay, (self.settings.paddingLeft, self.settings.paddingTop))  

        #     if keys[pygame.K_TAB]:
        #         self.currently_selected = None

        surface.blit(surf, pos)

   
    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            if self.currently_selected == "name":
                if event.type != pygame.K_BACKSPACE or event.key != pygame.K_RETURN:
                    if event.type == pygame.KEYUP:
                        if pygame.key.name(event.key) in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]:
                            self.items[self.item_index].name += event.unicode
            if self.currently_selected == "cost":
                if event.type != pygame.K_BACKSPACE or event.key != pygame.K_RETURN:
                    if event.type == pygame.KEYUP:
                        if pygame.key.name(event.key) in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                            self.items[self.item_index].cost = int(str(self.items[self.item_index].pay) + event.unicode)
            if self.currently_selected == "upc":
                if event.type != pygame.K_BACKSPACE or event.key != pygame.K_RETURN:
                    if event.type == pygame.KEYUP:
                        if pygame.key.name(event.key) in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]:
                            self.items[self.item_index].upc += event.unicode
            if self.currently_selected == "link":
                if event.type != pygame.K_BACKSPACE or event.key != pygame.K_RETURN:
                    if event.type == pygame.KEYUP:
                        if pygame.key.name(event.key) in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]:
                            self.items[self.item_index].link += event.unicode

    def show_save_error_message(self, surface: pygame.SurfaceType):
        first_line_render = self.font.render("Unsaved changes", True, self.settings.hoverText)
        second_line_render = self.font.render("Press *Ctrl S* to save", True, self.settings.hoverText)

        height = first_line_render.get_height() + second_line_render.get_height() + self.settings.paddingBottom + self.settings.paddingTop + self.settings.paddingBottom
        width = max(first_line_render.get_width(), second_line_render.get_width()) + self.settings.paddingLeft + self.settings.paddingRight

        surf = pygame.Surface((width, height))
        surf.fill("red")

        surf.blit(first_line_render, (self.settings.paddingLeft, self.settings.paddingTop))
        surf.blit(second_line_render, (self.settings.paddingLeft, self.settings.paddingTop+first_line_render.get_height()+self.settings.paddingTop))

        surface.blit(surf, (surface.get_width()-width-5, surface.get_height()-height-5))

    def save_to_file(self):
        with open("Config\\items.json", "w") as file:
            json.dump({"items": [item.__json__() for item in self.items]}, file)

    def change_crop_data(self, surface: pygame.SurfaceType, index: int):
        surf = pygame.surface.Surface((surface.get_width()//2, surface.get_height()//4))

        image_file_path_label = self.font.render("Image Path: ", True, self.settings.hoverText)
        
        image_path = self.font.render(self.items[index].image_path, True, self.settings.textColor)
        image_rect = image_path.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+image_file_path_label.get_width(), self.settings.paddingTop))
        image_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - image_file_path_label.get_width()
        
        surface.blit(surf, (surface.get_width()//2 - surf.get_width()//2, surface.get_height()//2 - surf.get_height()//2))
        # if name_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= name_rect.x+name_rect.width+pos[0] and name_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= name_rect.y+name_rect.height+pos[1]+35:
        #     name_bg = self.settings.hoverForeground
        #     name_text_color = self.settings.hoverText

        #     if pygame.mouse.get_pressed()[0]:
        #         self.currently_selected = "name"

        # else:
        #     name_bg = self.settings.foreground
        #     name_text_color = self.settings.textColor

        # if self.currently_selected == "name":
        #     name_bg = self.settings.selectedForeground
        #     name_text_color = self.settings.selectedText

        #     if keys[pygame.K_BACKSPACE]:
        #         self.employees[employee_index].name = self.employees[employee_index].name[:-1]
        #     elif keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
        #         self.employees[employee_index].editing = False
        #         self.currently_selected = None
        #     elif keys[pygame.K_SPACE]:
        #         self.employees[employee_index].name += " "
        #     elif keys[pygame.K_TAB]:
        #         self.currently_selected = None        


    def draw(self, surface: pygame.Surface):
        employee_viewport = pygame.Surface((self.width, self.height))
        employee_viewport.fill(self.settings.foreground)

        if self.item_generated_time != os.path.getmtime("Config\\employees.json"):
            self.generate_items()
            self.item_generated_time = os.path.getmtime("Config\\employees.json")

        previous_width = self.settings.paddingLeft
        y = self.settings.paddingTop
        for employee in self.items:
            employee_graphic = InventoryGraphic(self.x+previous_width, y, employee, self.settings)
            employee_graphic.draw(employee_viewport, self)

            previous_width += employee_graphic.width + self.settings.paddingLeft

            if previous_width + employee_graphic.width > self.width:
                previous_width = self.settings.paddingLeft
                y += employee_graphic.height + self.settings.paddingTop + self.settings.paddingBottom

            if employee.editing:
                self.draw_edit_window(employee_viewport, self.items.index(employee))
                self.item_index = self.items.index(employee)

            else:
                self.image = None

        if self.items != self.get_from_file_items():
            self.show_save_error_message(employee_viewport)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
            self.save_to_file()

        surface.blit(employee_viewport, (self.x, self.y))
