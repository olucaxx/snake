import pygame
import sys
import random

from snake import Snake

# config
SCREEN_SIZE = 20
SCALE = 32
TILES_GAP = 12

# init 
pygame.init()
pygame.display.set_caption("snake the game")
screen = pygame.display.set_mode((SCREEN_SIZE * SCALE, SCREEN_SIZE * SCALE))
clock = pygame.time.Clock()

pygame.font.init()
death_font = pygame.font.SysFont('arial', 48)
buttons_font = pygame.font.SysFont('arial', 18)

running = True

grid = {(y, x) for y in range(SCREEN_SIZE) for x in range(SCREEN_SIZE)}

pending_moves = []

def spawn_food(grid, snake_body):
    availiable = grid - set(snake_body)
    return random.choice(tuple(availiable))


while running:   
    alive = True
    snake = Snake(SCREEN_SIZE)
    food = spawn_food(grid, snake.body_sections)
    fps = 5 # vai aumentar ate 10 
    pending_moves.clear()

    while alive:    
        # - EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
                
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    if len(pending_moves) < 3: # permite ate dois comandos na fila
                        pending_moves.append(event.key)

        # - LOGICA DO JOGO
        if pending_moves:
            snake.change_direction(pending_moves.pop(0))

        if not snake.move(SCREEN_SIZE): # snake.move verifica se ela esta viva
            alive = False

        if snake.body_sections[0] == food:
            food = spawn_food(grid, snake.body_sections)
            snake.has_growth += 1

            if fps < 10:
                fps = min(10, 5 + (len(snake.body_sections) - 5) * 0.33)


        # - RENDERIZAR
        screen.fill((0,0,0))

        # render food
        pygame.draw.rect(
                        screen,
                        (255,0,0), 
                        ((food[1] * SCALE) + TILES_GAP / 2, 
                        (food[0] * SCALE) + TILES_GAP / 2, 
                        SCALE - TILES_GAP, 
                        SCALE - TILES_GAP)
                    )

        # render snake
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
        clock.tick(fps)
    
    score = len(snake.body_sections) - 5
    death_text = death_font.render(f"Score: {score}", False, (255,255,255))
    death_text_rect = death_text.get_rect(center=(SCREEN_SIZE*SCALE // 2, SCREEN_SIZE*SCALE // 2.25))

    buttons_text = buttons_font.render("ESC: sair  |  ENTER: jogar novamente",False, (255,255,255))
    buttons_text_rect = buttons_text.get_rect(center=(SCREEN_SIZE*SCALE / 2, SCREEN_SIZE*SCALE / 1.75))
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    waiting = False

                if event.key == pygame.K_RETURN:
                    waiting = False
        
        screen.fill((0,0,0))
        screen.blit(death_text, death_text_rect)
        screen.blit(buttons_text, buttons_text_rect)
        pygame.display.flip()
        clock.tick(30)


pygame.quit()
sys.exit()
