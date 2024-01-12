import pygame
import os


class Player:
    def __init__(self, screen, width, height):
        self.x_pos = width // 2
        self.y_pos = height * .9
        self.health = 3
        self.score = 0
        self.screen = screen
        self.screen_width = width
        self.tank_width = 100
        self.tank_height = 50
        self.move_speed = 20
        self.image = pygame.Rect(self.x_pos, self.y_pos, self.tank_width, self.tank_height)

    def update(self):
        self.image = pygame.Rect(self.x_pos, self.y_pos, self.tank_width, self.tank_height)
        pygame.draw.rect(self.screen, 'white', self.image)

    def move(self, direction):
        if direction == -1 and self.x_pos >= 0:
            self.x_pos += self.move_speed * direction
        if direction == 1 and self.x_pos <= self.screen_width - self.tank_width:
            self.x_pos += self.move_speed * direction
