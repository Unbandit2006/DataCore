import pygame
import widgets
import row_sidebar
import employee

settings = widgets.Settings.from_json_file("Config\\settings.json")

pygame.init()

window = pygame.display.set_mode([settings.width, settings.height], pygame.RESIZABLE)
clock = pygame.time.Clock()
dt = 0
pygame.display.set_caption("DataCore Demo App")

row = row_sidebar.RowSidebar(settings)
row.add_tab("Tab1", employee.EmployeeManagement)
row.add_tab("Tab2", None)
row.add_tab("Tab3", None)

running = True
while running:
    settings.check_changes()

    window.fill(settings.background)

    row.settings = settings
    row.draw(window)

    pygame.display.update()
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
