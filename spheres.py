import pygame
import random

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
        self.image = pygame.transform.scale(pygame.image.load('./Assets/sphere.png'),
                                            (self.radius * 2, self.radius * 2))
        self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.tail_1 = (-100, -100)
        self.tail_2 = (-100, -100)
        self.tail_3 = (-100, -100)
        self.tail_4 = (-100, -100)
        self.tail_5 = (-100, -100)
        self.tail_6 = (-100, -100)

    def update(self):
        # Checks if the Sphere is visible on the screen or not
        if self.y_pos > 0:
            # Draws red circles for the tail of the sphere
            pygame.draw.circle(self.screen, 'red', self.tail_1, self.radius * .8)
            pygame.draw.circle(self.screen, 'red', self.tail_2, self.radius * .6)
            pygame.draw.circle(self.screen, 'red', self.tail_3, self.radius * .5)
            pygame.draw.circle(self.screen, 'red', self.tail_4, self.radius * .4)
            pygame.draw.circle(self.screen, 'red', self.tail_5, self.radius * .3)
            pygame.draw.circle(self.screen, 'red', self.tail_6, self.radius * .2)

            # Draws slightly smaller orange circles that will make the red ones appear as outlines
            pygame.draw.circle(self.screen, 'orange', self.tail_1, self.radius * .5)
            pygame.draw.circle(self.screen, 'orange', self.tail_2, self.radius * .45)
            pygame.draw.circle(self.screen, 'orange', self.tail_3, self.radius * .4)
            pygame.draw.circle(self.screen, 'orange', self.tail_4, self.radius * .25)
            pygame.draw.circle(self.screen, 'orange', self.tail_5, self.radius * .2)
            pygame.draw.circle(self.screen, 'orange', self.tail_6, self.radius * .15)

            # Draws the sphere image to the screen
            self.screen.blit(self.surface, (self.x_pos - self.radius, self.y_pos - self.radius))
            self.screen.blit(self.image, (self.x_pos - self.radius, self.y_pos - self.radius))

        else:
            # If the sphere is not visible this draws a line at the top of the screen to indicate its postion
            pygame.draw.line(self.screen, 'brown', (self.x_pos - self.radius, 5), (self.x_pos + self.radius, 5), 5)
            pygame.draw.line(self.screen, 'red', (self.x_pos - self.radius, 0), (self.x_pos + self.radius, 0), 5)

    def move(self):
        # Checks if the sphere made contact with a wall and inverts its x_vel if it did to bounce back
        if self.x_pos < self.radius / 2:
            self.x_vel *= -1
        elif self.x_pos > self.screen_width - self.radius:
            self.x_vel *= -1

        # Calculates the tail circles positions prior to updating the spheres position
        self.calculate_tail()

        # Updates the spheres position based on the remaining velocity
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        # Dampening the velocity until it evently reaches 0
        self.y_vel *= .98
        self.x_vel *= .98

        # Applying Gravity to the sphere
        self.y_pos += self.gravity

    def calculate_tail(self):

        # Checks if the sphere is traveling up to avoid the tail being to spaced out
        if self.y_vel < -self.gravity:
            self.tail_6 = self.tail_5
            self.tail_5 = self.tail_4
            self.tail_4 = self.tail_3
            self.tail_3 = self.tail_2
            self.tail_2 = self.tail_1
            self.tail_1 = (self.x_pos, self.y_pos)

        # If the sphere is traveling down applies a random number to the x to give it a flicker
        elif self.y_vel > -self.gravity and self.gravity != 0:
            self.tail_6 = (self.tail_5[0] + random.randint(-2, 2), self.tail_5[1] - 5)
            self.tail_5 = (self.tail_4[0] + random.randint(-2, 2), self.tail_4[1] - 5)
            self.tail_4 = (self.tail_3[0] + random.randint(-2, 2), self.tail_3[1] - 5)
            self.tail_3 = (self.tail_2[0] + random.randint(-2, 2), self.tail_2[1] - 5)
            self.tail_2 = (self.tail_1[0] + random.randint(-2, 2), self.tail_1[1] - 7)
            self.tail_1 = (self.x_pos, self.y_pos - 7)


class Explosion:
    def __init__(self, screen, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.iteration = 1
        self.screen = screen
        self.image_1 = pygame.transform.scale(pygame.image.load('./Assets/explosion_1.png'), (30, 30))
        self.image_2 = pygame.transform.scale(pygame.image.load('./Assets/explosion_2.png'), (40, 40))
        self.image_3 = pygame.transform.scale(pygame.image.load('./Assets/explosion_3.png'), (50, 50))
        self.image_4 = pygame.transform.scale(pygame.image.load('./Assets/explosion_4.png'), (60, 60))

    def update(self):
        # Draws the explosion animation to the screen based on how long it has existed for
        if self.iteration <= 4:
            self.screen.blit(self.image_1, (self.x_pos - 5, self.y_pos - 10))
        elif self.iteration <= 8:
            self.screen.blit(self.image_2, (self.x_pos - 10, self.y_pos - 20))
        elif self.iteration <= 12:
            self.screen.blit(self.image_3, (self.x_pos - 15, self.y_pos - 30))
        elif self.iteration <= 16:
            self.screen.blit(self.image_4, (self.x_pos - 20, self.y_pos - 40))

        # Updates the iteration so it can draw the correct image on the next go around
        self.iteration += 1
