import pygame
import numpy as np
import sys
from colorsys import hsv_to_rgb

# config
WIDTH = 100
HEIGHT = 50
SCALE = 10
FPS = 60

# init 
pygame.init()
pygame.display.set_caption("sand simulation")
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
clock = pygame.time.Clock()

# memoria da tela, onde os pixeis ficam armazenados, -1 = vazio e entre 0 e 360 = cor hue
world = np.full(shape=(HEIGHT, WIDTH), fill_value=-1)

# lookup table para armazenar os valores rgb do hue
LUT = np.zeros((361,3), dtype=np.uint8)
for hue in range(361):
    (r, g, b) = hsv_to_rgb(hue/360, 1, 1)
    LUT[hue] = (r*255, g*255, b*255)

hue_value = 0 # armazenar qual "posicao" do hue estamos

running = True
pressing = False

while running:        
    # - EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pressing = True

        if event.type == pygame.MOUSEBUTTONUP:
            pressing = False

    # - POSICAO MOUSE
    mouse_x, mouse_y = pygame.mouse.get_pos()

    world_x = mouse_x // SCALE
    world_y = mouse_y // SCALE

    # - COLOCAR AREIA
    if pressing and 0 <= world_x < WIDTH and 0 <= world_y < HEIGHT:
        world[world_y][world_x] = 0

    # - RENDER WORLD
    if hue_value > 360: # garante o loop da roda de cores
        hue_value = 0

    screen.fill((0,0,0)) # pinta toda a SCREEN nao o world

    pixel_y, pixel_x = np.where(world >= 0)
    pixels = list(zip(pixel_y, pixel_x))

    for y, x in pixels:
        print(world[y][x])
        pygame.draw.rect(
                    screen,
                    LUT[world[y][x]], 
                    (x * SCALE, y * SCALE, SCALE, SCALE)
                )

    # - RENDER POSICAO DO MOUSE
    if 0 <= world_x < WIDTH and 0 <= world_y < HEIGHT:
        pygame.draw.rect(
            screen,
            LUT[hue_value],
            (world_x * SCALE, world_y * SCALE, SCALE, SCALE)
        )
    hue_value+=1

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
