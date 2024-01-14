import pygame
import random


class PowerUp:
    def __init__(self, screen, power_up, width):
        self.screen = screen
        self.gravity = 3
        self.x_pos = random.randint(50, width - 50)
        self.y_pos = -20
        self.height = 20
        self.width = 20
        self.power = power_up
        if power_up == 1:
            image = pygame.image.load('./Assets/heart.png')
            self.image = pygame.transform.scale(image, (self.width, self.height))
        elif power_up == 2:
            image = pygame.image.load('./Assets/snowflake.png')
            self.image = pygame.transform.scale(image, (self.width, self.height))
        elif power_up == 3:
            image = pygame.image.load('./Assets/bullets.png')
            self.image = pygame.transform.scale(image, (self.width, self.height))


    def move(self):
        self.y_pos += self.gravity

    def update(self):
        self.screen.blit(self.image, (self.x_pos, self.y_pos))
