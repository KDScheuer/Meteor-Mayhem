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
        image = pygame.image.load('./Assets/tank.png')
        self.image = pygame.transform.scale(image, (self.tank_width, self.tank_height))
        self.aim_target = pygame.Rect(self.x_pos, self.y_pos, 20, 20)  # TODO Replace with Target Image
        self.aim_point = (0, 0)
        self.barrel_angle = 90
        self.time_since_last_shot = 0

    def update(self):
        """Draws Player to Screen"""
        self.screen.blit(self.image, (self.x_pos, self.y_pos))
        pygame.draw.rect(self.screen, 'red', self.aim_target)
        pygame.draw.line(self.screen, (117, 71, 18), self.center, self.aim_point, 5)
        self.time_since_last_shot -= 1

    def move_tank(self, direction):
        """Moves Players Tank (-1 = Left) (1 = Right)"""
        # Changes the X Position of the Tank Based on Movement Speed and Direction of Travel (Keep on Screen)
        if direction == -1 and self.x_pos >= 0:
            self.x_pos += self.move_speed * direction
        if direction == 1 and self.x_pos <= self.screen_width - self.tank_width:
            self.x_pos += self.move_speed * direction


    def move_barrel(self):
        """Moves the Tank Barrel to Point at Mouse"""
        # Calculates Where the Beginning of the Barrel is
        self.center = ((self.x_pos + self.tank_width / 2), (self.y_pos + self.tank_height / 2))

        # Keeps Player from Aiming and Shooting the Ground
        if self.aim_point[1] <= self.y_pos + self.tank_height / 2:
            self.barrel_angle = math.atan2(self.aim_point[1] - self.center[1], self.aim_point[0] - self.center[0])
            self.aim_target = pygame.Rect((self.aim_point[0] - 10, self.aim_point[1] - 10), (20, 20))

        # Calculates a 50px line for the Tanks Barrel
        self.aim_point = (self.center[0] + 50 * math.cos(self.barrel_angle),
                          self.center[1] + 50 * math.sin(self.barrel_angle))
