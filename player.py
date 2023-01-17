import pygame

up_limit = 0
down_limit = 400
left_limit = 0
right_limit = 400


class Player:
    def __init__(self, x, y, p_width, p_height, color):
        self.x = x
        self.y = y
        self.width = p_width
        self.height = p_height
        self.color = color
        self.rect = (x, y, p_width, p_height)
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.x > left_limit:
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and self.x < right_limit:
            self.x += self.vel
        if keys[pygame.K_UP] and self.y > up_limit:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < down_limit:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)