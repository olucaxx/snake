import pygame
import sys

from snake import Snake

# config
WIDTH = 20
HEIGHT = WIDTH
SCALE = 16
TILES_GAP = 6
FPS = 5

# init 
pygame.init()
pygame.display.set_caption("snake the game")
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
clock = pygame.time.Clock()

running = True

snake = Snake(WIDTH)

pending_moves = []

while running:        
    # - EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if len(pending_moves) < 3: # permite ate dois comandos na fila
                pending_moves.append(event.key)

    # - LOGICA DO JOGO
    if pending_moves:
        snake.change_direction(pending_moves.pop(0))

    if not snake.move(WIDTH): # snake.move verifica se ela esta viva
        running = False

    # - RENDERIZAR
    screen.fill((0,0,0))

    for i, (y, x) in enumerate(snake.body_sections):
        sx = (x * SCALE) + TILES_GAP / 2
        sy = (y * SCALE) + TILES_GAP / 2
        sw = SCALE - TILES_GAP 
        sh = SCALE - TILES_GAP 

        if i != 0:
            dy = y - snake.body_sections[i-1][0]
            dx = x - snake.body_sections[i-1][1] 

            if dy < 0:
                sh += TILES_GAP 
            
            elif dy > 0:
                sh += TILES_GAP 
                sy -= TILES_GAP 
            
            elif dx < 0:
                sw += TILES_GAP 
            
            elif dx > 0:
                sw += TILES_GAP 
                sx -= TILES_GAP 

        pygame.draw.rect(
                    screen,
                    (0,255,0), 
                    (sx, sy, sw, sh)
                )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
