import pygame
import math
import random
from player import Player
from shots import Shot
from spheres import Sphere

# Global Variables
WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


def game_loop():
    running = True
    player = Player(SCREEN, WIDTH, HEIGHT)
    shots = []
    initial_sphere = Sphere(SCREEN, WIDTH, WIDTH / 2, HEIGHT / 2, 0, 0)
    spheres = [initial_sphere]

    while running:
        # Gets Keys Pressed and Moves the Player Accordingly
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            player.move_tank(-1)
        if keys_pressed[pygame.K_d]:
            player.move_tank(1)

        # Gets the Position of the Mouse and Moves the Barrel Angle to Match
        player.aim_point = pygame.mouse.get_pos()
        player.move_barrel()

        # Checks if Player Quit the Game or Fired a Shot
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and player.time_since_last_shot <= 0:
                new_shot = Shot(SCREEN, player.aim_point, player.barrel_angle)
                shots.append(new_shot)
                player.time_since_last_shot = 5

        for shot in shots:
            shot.move_shot()

        for sphere in spheres:
            for shot in shots:
                distance = math.sqrt((sphere.x_pos - shot.end_x_pos) ** 2 + (sphere.y_pos - shot.end_y_pos) ** 2)
                if distance < sphere.radius:
                    sphere_hit(shot, sphere, spheres)
                    shots.remove(shot)
                    del shot
                    continue

                elif shot.start_x_pos < 0 or shot.start_x_pos > WIDTH:
                    shots.remove(shot)
                    del shot
            sphere.move()

            # TODO DELETE THIS AFTER DAMAGE IS ADDED THIS IS FOR TESTING ONLY
            if sphere.y_pos > HEIGHT:
                spheres.remove(sphere)
                del sphere

        # Call to Update Screen and Sets FPS
        update_screen(player, shots, spheres)
        CLOCK.tick(60)


def sphere_hit(shot, sphere, spheres):
    # Calculate Shots X and Y Velocities
    shot_x_vel = shot.speed * math.cos(shot.shot_angle)
    shot_y_vel = shot.speed * math.sin(shot.shot_angle)

    # Calculate Angle of Impact
    impact_angle = math.atan2(shot_y_vel, shot_x_vel)

    # Calculate Spheres New Velocity
    new_vel_x = sphere.x_vel + shot.power * math.cos(impact_angle)
    new_vel_y = sphere.y_vel + shot.power * math.sin(impact_angle)


    # Update Spheres Velocities
    sphere.x_vel = new_vel_x
    sphere.y_vel = new_vel_y
    if len(spheres) < 4 and random.randint(1, 4) == 1:
        new_sphere = Sphere(SCREEN, WIDTH, sphere.x_pos, sphere.y_pos, random.randint(-5, 5),
                            new_vel_y + random.randint(-5, 0))
        spheres.append(new_sphere)
    elif len(spheres) >= 4 and random.randint(1, 8) == 1:
        new_sphere = Sphere(SCREEN, WIDTH, sphere.x_pos, sphere.y_pos, random.randint(-5, 5),
                            new_vel_y + random.randint(-5, 0))
        spheres.append(new_sphere)

    sphere.times_hit += 1

    if sphere.times_hit == 7 and len(spheres) > 1:
        spheres.remove(sphere)
        del sphere


def update_screen(player, shots, spheres):
    """Calls all update functions and methods to draw everything to the screen"""
    SCREEN.fill('black')
    for shot in shots:
        shot.update()
    for sphere in spheres:
        sphere.update()
    player.update()
    pygame.display.update()


def main():
    pygame.mouse.set_visible(0)
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
