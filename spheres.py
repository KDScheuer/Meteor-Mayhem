import pygame
import time

class Sphere:
    def __init__(self, screen, screen_width, x_pos, y_pos, x_vel=0, y_vel=0, grav=3):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.radius = 25
        self.gravity = grav
        self.times_hit = 0
        self.screen_width = screen_width
        self.frozen = False
        self.frozen_time = 0

    def update(self):
        if self.y_pos > 0:
            pygame.draw.circle(self.screen, 'blue', (self.x_pos, self.y_pos), self.radius)
        else:
            pygame.draw.line(self.screen, 'blue', (self.x_pos - self.radius, 5), (self.x_pos + self.radius, 5), 5)

    def move(self):
        if self.x_pos < self.radius / 2:
            self.x_vel *= -1
        elif self.x_pos > self.screen_width - self.radius:
            self.x_vel *= -1

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        self.y_vel *= .98
        self.x_vel *= .98
        self.y_pos += self.gravity


class Explosion:
    def __init__(self, screen, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.iteration = 1
        self.screen = screen
        self.image_1 = pygame.rect.Rect((self.x_pos - 5, self.y_pos - 10), (10, 10))
        self.image_2 = pygame.rect.Rect((self.x_pos - 10, self.y_pos - 20), (20, 20))
        self.image_3 = pygame.rect.Rect((self.x_pos - 15, self.y_pos - 30), (30, 30))
        self.image_4 = pygame.rect.Rect((self.x_pos - 20, self.y_pos - 40), (40, 40))

    def update(self):
        if self.iteration == 1:
            pygame.draw.rect(self.screen, 'black', self.image_1)
        elif self.iteration == 2:
            pygame.draw.rect(self.screen, 'black', self.image_2)
        elif self.iteration == 3:
            pygame.draw.rect(self.screen, 'black', self.image_3)
        elif self.iteration == 4:
            pygame.draw.rect(self.screen, 'black', self.image_4)

        self.iteration += 1
