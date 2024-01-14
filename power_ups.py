import pygame
import random


class PowerUp:
    def __init__(self, screen, power_up, width):
        self.screen = screen
        self.gravity = 4
        self.x_pos = random.randint(50, width - 50)
        self.y_pos = -20
        self.height = 20
        self.width = 20
        self.power = power_up
        self.color = 'white'
        if power_up == 1:
            # Add Health
            self.image = pygame.Rect((self.x_pos, self.y_pos), (self.width, self.height))
            self.color = 'red'
        elif power_up == 2:
            self.image = pygame.Rect((self.x_pos, self.y_pos), (self.width, self.height))
            self.color = 'blue'
            # Freeze (Freeze Time for 3 Seconds)
            pass
        elif power_up == 3:
            self.image = pygame.Rect((self.x_pos, self.y_pos), (self.width, self.height))
            self.color = 'yellow'
            # Rapid Fire (Fires a shitton of rounds automatically for 3 Seconds)
            pass

    def move(self):
        self.y_pos += self.gravity
        self.image = pygame.Rect((self.x_pos, self.y_pos), (20, 20))

    def update(self):
        pygame.draw.rect(self.screen, self.color, self.image)
