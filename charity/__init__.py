import pygame.image
import clarity
import pygame
import json
import os

class EmployeeData:
    def __init__(self, information):
        self.name = information["firstName"] + " " + information["lastName"]
        self.pay = information["pay"]
        self.title = information["title"]
        self.role = information["role"]
        self.image_path = information["image"]
        self.image_data = information["cropData"]

        self.editing = False

    def __repr__(self) -> str:
        return f"<Employee {self.name}>"


class EmployeeGraphic(clarity.Widget):
    def __init__(self, x, y, data: EmployeeData, settings: clarity.Settings, font: pygame.font.FontType = pygame.font.SysFont("Consolas", 15)):
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

        pay_render_height = self.settings.paddingTop + self.settings.paddingBottom + self.font.render("Pay: $"+str(self.data.pay), True, self.settings.textColor).get_height()
        pay_render_width = self.settings.paddingLeft + self.settings.paddingRight + self.font.render("Pay: $"+str(self.data.pay), True, self.settings.textColor).get_width()
        text_width = max(text_width, pay_render_width)
        text_height += pay_render_height

        title_render_height = self.settings.paddingTop + self.settings.paddingBottom + self.font.render("Title: "+self.data.title, True, self.settings.textColor).get_height()
        title_render_width = self.settings.paddingLeft + self.settings.paddingRight + self.font.render("Title: "+self.data.title, True, self.settings.textColor).get_width()
        text_width = max(text_width, title_render_width)
        text_height += title_render_height

        role_render_height = self.settings.paddingTop + self.settings.paddingBottom + self.font.render("Role: "+self.data.role, True, self.settings.textColor).get_height()
        role_render_width = self.settings.paddingLeft + self.settings.paddingRight + self.font.render("Role: "+self.data.role, True, self.settings.textColor).get_width()
        text_width = max(text_width, role_render_width)
        text_height += role_render_height

        self.width += max(self.width, text_width)
        self.height = max(self.height, text_height)

    def resize_image(self):
        self.image = pygame.image.load(self.data.image_path)
        self.image = self.image.subsurface(self.data.image_data[0], self.data.image_data[1], self.data.image_data[2], self.data.image_data[3])
        self.image = pygame.transform.smoothscale(self.image, (100, 100))

    def draw(self, surface: pygame.Surface, widget_parent: clarity.Widget):
        employee_surface = pygame.Surface((self.width, self.height))
        employee_surface.fill(self.settings.background)

        edit_color = self.settings.foreground
        edit_text_color = self.settings.textColor

        if self.data.editing:
            edit_color = self.settings.hoverForeground
            edit_text_color = self.settings.hoverText

        if self.image is None:
            self.resize_image()
        employee_surface.blit(self.image, (self.settings.paddingLeft, self.settings.paddingTop))

        name_render = self.font.render("Name: "+self.data.name, True, self.settings.selectedText)
        pay_render = self.font.render("Pay: $"+str(self.data.pay), True, self.settings.selectedText)
        title_render = self.font.render("Title: "+self.data.title, True, self.settings.selectedText)
        role_render = self.font.render("Role: "+self.data.role, True, self.settings.selectedText)

        y = self.settings.paddingTop
        employee_surface.blit(name_render, (self.settings.paddingLeft+100+self.settings.paddingRight, self.settings.paddingTop))
        y += name_render.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        employee_surface.blit(pay_render, (self.settings.paddingLeft+100+self.settings.paddingRight, y))
        y += pay_render.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        employee_surface.blit(title_render, (self.settings.paddingLeft+100+self.settings.paddingRight, y))
        y += title_render.get_height() + self.settings.paddingTop + self.settings.paddingBottom

        employee_surface.blit(role_render, (self.settings.paddingLeft+100+self.settings.paddingRight, y))

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
        if edit_rect.x + x_offset <= pygame.mouse.get_pos()[0] <= edit_rect.x+edit_rect.width + x_offset:
            if edit_rect.y+y_offset <= pygame.mouse.get_pos()[1] <= edit_rect.y+edit_rect.height+y_offset:
                edit_color = self.settings.hoverForeground
                edit_text_color = self.settings.hoverText

                if pygame.mouse.get_pressed()[0]:
                    self.data.editing = True

        edit_text = self.font.render("Edit", True, edit_text_color)
        pygame.draw.rect(employee_surface, edit_color, edit_rect)
        employee_surface.blit(edit_text, (edit_rect.x+self.settings.paddingLeft, edit_rect.y+self.settings.paddingRight))

        surface.blit(employee_surface, (self.x, self.y))


class EmployeeManagement(clarity.Widget):
    def __init__(self, settings: clarity.Settings):
        super().__init__(0, 0, 0, 0, settings)

        self.employees = []
        self.employee_generated_time = None
        self.image = None
        self.font = pygame.font.SysFont("Consolas", 15)

    def generate_employees(self):
        with open("Config\\employees.json") as file:
            employees = json.load(file)["employees"]

            for employee in employees:
                self.employees.append(EmployeeData(employee))

    def resize_image(self, employee_index: int):
        self.image = pygame.image.load(self.employees[employee_index].image_path)
        self.image = self.image.subsurface(self.employees[employee_index].image_data[0], self.employees[employee_index].image_data[1], self.employees[employee_index].image_data[2], self.employees[employee_index].image_data[3])
        self.image = pygame.transform.smoothscale(self.image, (100, 100))

    def draw_edit_window(self, surface: pygame.Surface, employee_index: int):
        width = 0
        height = 0

        width += self.settings.paddingLeft + 100 + self.settings.paddingRight
        height += self.settings.paddingTop + 100 + self.settings.paddingBottom

        text_height = self.settings.paddingTop + self.settings.paddingBottom
        text_width = self.settings.paddingLeft + self.settings.paddingLeft

        name_render_height = text_height + self.font.render("Name: "+self.employees[employee_index].name, True, self.settings.textColor).get_height()
        name_render_width = text_width + self.font.render("Name: "+self.employees[employee_index].name, True, self.settings.textColor).get_width()
        text_width = max(text_width, name_render_width)
        text_height += name_render_height

        pay_render_height = 2*(self.settings.paddingTop + self.settings.paddingBottom) + self.font.render("Pay: $"+str(+self.employees[employee_index].pay), True, self.settings.textColor).get_height()
        pay_render_width = 2*(self.settings.paddingLeft + self.settings.paddingRight) + self.font.render("Pay: $"+str(self.employees[employee_index].pay), True, self.settings.textColor).get_width()
        text_width = max(text_width, pay_render_width)
        text_height += pay_render_height

        title_render_height = 2*(self.settings.paddingTop + self.settings.paddingBottom) + self.font.render("Title: "+self.employees[employee_index].title, True, self.settings.textColor).get_height()
        title_render_width = 2*(self.settings.paddingLeft + self.settings.paddingRight) + self.font.render("Title: "+self.employees[employee_index].title, True, self.settings.textColor).get_width()
        text_width = max(text_width, title_render_width)
        text_height += title_render_height

        role_render_height = 2*(self.settings.paddingTop + self.settings.paddingBottom) + self.font.render("Role: "+self.employees[employee_index].role, True, self.settings.textColor).get_height()
        role_render_width = 2*(self.settings.paddingLeft + self.settings.paddingRight) + self.font.render("Role: "+self.employees[employee_index].role, True, self.settings.textColor).get_width()
        text_width = max(text_width, role_render_width)
        text_height += role_render_height

        width += max(width, text_width)
        height = max(height, text_height)

        if self.image is None:
            self.resize_image(employee_index)

        surf = pygame.Surface((width, height))
        pos = ((self.width//2 - width//2), (self.height//2 - height//2))
        surf.fill(self.settings.background)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.employees[employee_index].editing = False

        y = self.settings.paddingTop

        name_label_render = self.font.render("Name: ", True, self.settings.selectedText)
        surf.blit(name_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        name_render = self.font.render("Name: "+self.employees[employee_index].name, True, self.settings.textColor)
        act_name = self.font.render(self.employees[employee_index].name, True, self.settings.textColor)
        name_rect = name_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+name_label_render.get_width(), y))
        name_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - name_label_render.get_width()
        
        if name_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= name_rect.x+name_rect.width+pos[0] and name_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= name_rect.y+name_rect.height+pos[1]+35:
            name_bg = self.settings.hoverForeground
            name_text_color = self.settings.hoverText
        else:
            name_bg = self.settings.foreground
            name_text_color = self.settings.textColor
        
        act_name = self.font.render(self.employees[employee_index].name, True, name_text_color)
        pygame.draw.rect(surf, name_bg, name_rect)
        surf.blit(act_name, (name_rect.x, name_rect.y))

        y += int(name_rect.height) + self.settings.paddingBottom + self.settings.paddingTop

        pay_label_render = self.font.render("Pay: $", True, self.settings.selectedText)
        surf.blit(pay_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        pay_render = self.font.render("Pay: $"+str(self.employees[employee_index].pay), True, self.settings.textColor)
        act_pay = self.font.render(str(self.employees[employee_index].pay), True, self.settings.textColor)
        pay_rect = pay_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+pay_label_render.get_width(), y))
        pay_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - pay_label_render.get_width()

        if pay_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= pay_rect.x+pay_rect.width+pos[0] and pay_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= pay_rect.y+pay_rect.height+pos[1]+35:
            pay_bg = self.settings.hoverForeground
            pay_text_color = self.settings.hoverText
        else:
            pay_bg = self.settings.foreground
            pay_text_color = self.settings.textColor

        act_pay = self.font.render(str(self.employees[employee_index].pay), True, pay_text_color)
        pygame.draw.rect(surf, pay_bg, pay_rect)
        surf.blit(act_pay, (pay_rect.x, pay_rect.y))

        y += int(pay_rect.height) + self.settings.paddingBottom + self.settings.paddingTop

        title_label_render = self.font.render("Title: ", True, self.settings.selectedText)
        surf.blit(title_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        title_render = self.font.render("Title: "+str(self.employees[employee_index].title), True, self.settings.textColor)
        act_title = self.font.render(str(self.employees[employee_index].title), True, self.settings.textColor)
        title_rect = title_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+title_label_render.get_width(), y))
        title_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - title_label_render.get_width()

        if title_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= title_rect.x+title_rect.width+pos[0] and title_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= title_rect.y+title_rect.height+pos[1]+35:
            title_bg = self.settings.hoverForeground
            title_text_color = self.settings.hoverText
        else:
            title_bg = self.settings.foreground
            title_text_color = self.settings.textColor

        act_title = self.font.render(str(self.employees[employee_index].title), True, title_text_color)
        pygame.draw.rect(surf, title_bg, title_rect)
        surf.blit(act_title, (title_rect.x, title_rect.y))

        y += int(title_rect.height) + self.settings.paddingBottom + self.settings.paddingTop

        role_label_render = self.font.render("Role: ", True, self.settings.selectedText)
        surf.blit(role_label_render, (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100, y))
        role_render = self.font.render("Role: "+str(self.employees[employee_index].role), True, self.settings.textColor)
        act_role = self.font.render(str(self.employees[employee_index].role), True, self.settings.textColor)
        role_rect = role_render.get_rect(topleft=(self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+role_label_render.get_width(), y))
        role_rect.width = surf.get_width() - (self.settings.paddingLeft+self.settings.paddingRight+self.settings.paddingLeft+100+self.settings.paddingRight) - role_label_render.get_width()
        
        if role_rect.x+pos[0] <= pygame.mouse.get_pos()[0] <= role_rect.x+role_rect.width+pos[0] and role_rect.y+pos[1]+35 <= pygame.mouse.get_pos()[1] <= role_rect.y+role_rect.height+pos[1]+35:
            role_bg = self.settings.hoverForeground
            role_text_color = self.settings.hoverText
        else:
            role_bg = self.settings.foreground
            role_text_color = self.settings.textColor        

        act_role = self.font.render(str(self.employees[employee_index].role), True, role_text_color)
        pygame.draw.rect(surf, role_bg, role_rect)
        surf.blit(act_role, (role_rect.x, role_rect.y))

        y_area = surf.get_height() - self.settings.paddingBottom - self.settings.paddingTop - 100
        x_area = surf.get_width() - self.settings.paddingRight - self.settings.paddingLeft

        esc_render = self.font.render("Press *Esc* to save and exit", True, self.settings.selectedText)
        surf.blit(esc_render, (self.settings.paddingLeft+(x_area//2 - esc_render.get_width()//2), self.settings.paddingTop+self.settings.paddingBottom+100+(y_area//2 - esc_render.get_height()//2)))

        surf.blit(self.image, (self.settings.paddingLeft, self.settings.paddingTop))

        surface.blit(surf, pos)

    def draw(self, surface: pygame.Surface):
        employee_viewport = pygame.Surface((self.width, self.height))
        employee_viewport.fill(self.settings.foreground)

        if self.employee_generated_time != os.path.getmtime("Config\\employees.json"):
            self.generate_employees()
            self.employee_generated_time = os.path.getmtime("Config\\employees.json")

        previous_width = self.settings.paddingLeft
        y = self.settings.paddingTop
        for employee in self.employees:
            employee_graphic = EmployeeGraphic(self.x+previous_width, y, employee, self.settings)
            employee_graphic.draw(employee_viewport, self)

            previous_width += employee_graphic.width + self.settings.paddingLeft

            if previous_width + employee_graphic.width > self.width:
                previous_width = self.settings.paddingLeft
                y += employee_graphic.height + self.settings.paddingTop + self.settings.paddingBottom

            if employee.editing:
                self.draw_edit_window(employee_viewport, self.employees.index(employee))
            else:
                self.image = None

        surface.blit(employee_viewport, (self.x, self.y))


