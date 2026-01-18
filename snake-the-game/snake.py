import pygame

# mapeamento dos botoes
KEY_MAP = {
    pygame.K_UP:    (-1, 0),
    pygame.K_DOWN:  (1, 0),
    pygame.K_LEFT:  (0, -1),
    pygame.K_RIGHT: (0, 1),
} 

class Snake:
    def __init__(self, screen_size):
        middle = (screen_size // 2) - 1
        # garante que ela fique no centro, independente do tamanho da tela
        self.body_sections = [(middle, middle + x) for x in range(-2,3)]
        self.mov_direction = (0,-1)
        self.has_growth = 0

    def change_direction(self, key) -> None:
        new_direction = KEY_MAP.get(key)

        # garante que tenhamos um movimento valido
        if new_direction is not None: 
            # garante que voce nao consiga andar de volta em si mesmo
            if new_direction != (-self.mov_direction[0], -self.mov_direction[1]):
                self.mov_direction = new_direction

    def move(self, screen_size) -> bool:
        is_alive = True

        next_move = (
            self.body_sections[0][0] + self.mov_direction[0],
            self.body_sections[0][1] + self.mov_direction[1]
            )

        # verifica se bateu nos cantos da tela
        if not (0 <= next_move[0] < screen_size and
                0 <= next_move[1] < screen_size):
            is_alive = False

        # colisão com corpo, ignorando o rabo
        if next_move in self.body_sections[:-1]:
            is_alive = False
        
        self.body_sections.insert(0, next_move)
        if self.has_growth > 0:
            self.has_growth -= 1
            return is_alive
        
        self.body_sections.pop()
        return is_alive
