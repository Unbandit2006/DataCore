import pygame
pygame.init()

window = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

image_path = "Images\\danZ.jpg"
image = pygame.image.load(image_path)
image_rect = pygame.Rect(0, 0, 200, 200)

state = 0
crop_data = []

def draw_image():
    window.blit(image, (0, 0))

    image_rect.x = pygame.mouse.get_pos()[0] - image_rect.width/2
    image_rect.y = pygame.mouse.get_pos()[1] - image_rect.height/2
    pygame.draw.rect(window, (255, 0, 0), image_rect, 2)

def draw_cropped():
    subface = image.subsurface(crop_data[0], crop_data[1], crop_data[2], crop_data[3])
    subface = pygame.transform.smoothscale(subface, (100, 100))

    window.blit(subface, (0, 0))

running = True
while running:
    window.fill((0, 0, 0))

    if state == 0:
        draw_image()

    else:
        draw_cropped()

    clock.tick(60)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONUP:
            state = 1
            crop_data = [pygame.mouse.get_pos()[0]-image_rect.width/2, pygame.mouse.get_pos()[1]-image_rect.height/2, 200, 200]
            print(image_path + f": {crop_data}")
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                state = 0
                crop_data = []