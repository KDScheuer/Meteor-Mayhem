import pygame
import math


class Shot:
    def __init__(self, screen, aim_point, angle):
        self.start_x_pos = aim_point[0]
        self.start_y_pos = aim_point[1]
        self.end_x_pos = 0
        self.end_y_pos = 0
        self.shot_angle = angle
        self.length = 20
        self.speed = 20
        self.power = 10
        self.screen = screen

    def move_shot(self):
        self.end_x_pos = self.start_x_pos + self.length * math.cos(self.shot_angle)
        self.end_y_pos = self.start_y_pos + self.length * math.sin(self.shot_angle)

    def update(self):
        pygame.draw.line(self.screen, 'yellow', (self.start_x_pos, self.start_y_pos),
                         (self.end_x_pos, self.end_y_pos), 2)

        self.start_x_pos = self.start_x_pos + self.speed * math.cos(self.shot_angle)
        self.start_y_pos = self.start_y_pos + self.speed * math.sin(self.shot_angle)
