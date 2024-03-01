import pygame, sys
import DAV as dave
import DAVX as davex

pygame.init()
pygame.font.init()

debug = False
animation = True

for arg in sys.argv:
    if arg == "--debug":
        debug = True
        
    if arg == "--no-animation":
        animation = False


window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("DataCore")

clock = pygame.time.Clock()

deltatime = 0

drawable_surf = pygame.Surface((window.get_width()-10, window.get_height()-10))
sales = davex.Sales()

running = True
while running:
    window.fill("midnightblue")

    drawable_surf = pygame.Surface((window.get_width()-10, window.get_height()-10))
    drawable_surf.fill("#124f90")

    sales.draw(drawable_surf)

    window.blit(drawable_surf, (5, 5))

    deltatime = clock.tick(60)
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
                    
            