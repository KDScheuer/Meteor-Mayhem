import pygame
import math


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
        self.move_speed = 10
        self.center = ((self.x_pos + self.tank_width / 2), (self.y_pos + self.tank_height / 2))
        self.image = pygame.Rect(self.x_pos, self.y_pos, self.tank_width, self.tank_height) # TODO Replace with Tank Image
        self.aim_target = pygame.Rect(self.x_pos, self.y_pos, 20, 20) # TODO Replace with Target Image
        self.aim_point = (0, 0)

    def update(self):
        self.move_barrel()
        pygame.draw.rect(self.screen, 'white', self.image)
        pygame.draw.rect(self.screen, 'red', self.aim_target)

    def move_tank(self, direction):
        if direction == -1 and self.x_pos >= 0:
            self.x_pos += self.move_speed * direction
        if direction == 1 and self.x_pos <= self.screen_width - self.tank_width:
            self.x_pos += self.move_speed * direction

        self.image = pygame.Rect(self.x_pos, self.y_pos, self.tank_width, self.tank_height)

    def move_barrel(self):
        if self.aim_point[1] <= self.y_pos:
            self.aim_target = pygame.Rect(self.aim_point, (20, 20))

        self.center = ((self.x_pos + self.tank_width / 2), (self.y_pos + self.tank_height / 2))

        if math.hypot(self.aim_point[0] - self.center[0], self.aim_point[1] - self.center[1]) > 100:
            angle = math.atan2(self.aim_point[1] - self.center[1], self.aim_point[0] - self.center[0])
            self.aim_point = (self.center[0] + 100 * math.cos(angle), self.center[1] + 100 * math.sin(angle))

        pygame.draw.line(self.screen, 'white', self.center, self.aim_point, 5)
