import pygame
import numpy as np
import sys
import colorsys

# config
WIDTH = 120
HEIGHT = 60
SCALE = 10
FPS = 60

# init 
pygame.init()
pygame.display.set_caption("sand simulation")
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
clock = pygame.time.Clock()

# memoria da tela, onde os pixeis ficam armazenados, -1 = vazio e entre 0 e 360 = cor hue
world = np.full(shape=(HEIGHT, WIDTH), fill_value=-1)

running = True

while running:
    # - EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0)) # pinta de preto toda a tela

    # - RENDERIZAÇÃO
    ys, xs = np.where(world >= 0)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if world[y, x] == 1:
                pygame.draw.rect(
                    screen,
                    hsv(hue), 
                    (x * SCALE, y * SCALE, SCALE, SCALE)
                )

    # - MOUSE
    mx, my = pygame.mouse.get_pos()

    gx = mx // SCALE
    gy = my // SCALE

    # apenas se o mouse estiver dentro da tela
    if 0 <= gx < WIDTH and 0 <= gy < HEIGHT:
        
        # bloco vermelho pra mostrar a pos e print no terminal
        print(gx, gy)
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (gx * SCALE, gy * SCALE, SCALE, SCALE)
        )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
