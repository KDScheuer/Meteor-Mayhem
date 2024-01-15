import pygame
import math
import random
import sys
from player import Player
from shots import Shot
from spheres import Sphere, Explosion
from power_ups import PowerUp

# Global Variables
WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
BACKGROUND = pygame.transform.scale(pygame.image.load('./Assets/background.png'), (WIDTH, HEIGHT))
FPS = 60
SCREEN_SHAKE = 0
DISPLAY_CONTROLS = True
EXPLOSIONS = []
pygame.mixer.init()
CANNON_SOUND = pygame.mixer.Sound('./Assets/cannon.mp3')
EXPLOSION_SOUND = pygame.mixer.Sound('./Assets/explosion.wav')
POWER_UP_SOUND = pygame.mixer.Sound('./Assets/power-up.wav')
pygame.mixer.set_num_channels(200)
SOUND_CHANNELS = [pygame.mixer.Channel(i) for i in range(pygame.mixer.get_num_channels())]


def game_loop():
    running = True
    player = Player(SCREEN, WIDTH, HEIGHT)
    ground = player.y_pos + player.tank_height
    shots = []
    initial_sphere = Sphere(SCREEN, WIDTH, WIDTH / 2, HEIGHT / 2 + 50, 0, 0, 0)
    spheres = [initial_sphere]
    tick, time_played_seconds = 0, 0
    power_up_spawn_rate_seconds = 20
    power_ups = []
    freeze_active = False
    auto_fire_active = False
    game_over = False

    while running:
        global SCREEN_SHAKE

        CLOCK.tick(FPS)

        if game_over is True:
            quit_game = end_screen(player, shots, spheres, power_ups, game_over, ground)
            print(quit_game)
            if quit_game:
                pygame.quit()
                sys.exit()
            continue

        # Calculate Time the Game has been Running
        if tick == FPS:
            time_played_seconds += 1
            tick = 0
        else:
            tick += 1

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
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and player.time_since_last_shot <= 0:
                new_shot = Shot(SCREEN, player.aim_point, player.barrel_angle)
                new_shot.move_shot()
                shots.append(new_shot)
                player.time_since_last_shot = 5
                next((ch for ch in SOUND_CHANNELS if not ch.get_busy()), None).play(CANNON_SOUND)

        for shot in shots:
            shot.move_shot()

        for sphere in spheres:
            for shot in shots:
                distance = math.sqrt((sphere.x_pos - shot.end_x_pos) ** 2 + (sphere.y_pos - shot.end_y_pos) ** 2)
                if distance < sphere.radius:
                    sphere_hit(shot, sphere, spheres, player)
                    sphere.frozen = False
                    shots.remove(shot)
                    del shot
                    continue

                elif shot.start_x_pos < 0 or shot.start_x_pos > WIDTH:
                    shots.remove(shot)
                    del shot
            if freeze_active is True and sphere.frozen is True:
                continue
            else:
                sphere.move()

            if sphere.y_pos + sphere.radius > ground:

                player.health -= 1
                spheres.remove(sphere)
                explosion = Explosion(SCREEN, sphere.x_pos, sphere.y_pos + sphere.radius)
                EXPLOSIONS.append(explosion)
                SCREEN_SHAKE = 3
                next((ch for ch in SOUND_CHANNELS if not ch.get_busy()), None).play(EXPLOSION_SOUND)
                del sphere
            if len(spheres) == 0 or player.health == 0:
                game_over = True
                for shot in shots:
                    shots.remove(shot)
                player.x_pos = WIDTH // 2 - player.tank_width // 2
                player.y_pos = HEIGHT * .85

        if time_played_seconds % power_up_spawn_rate_seconds == 0 and time_played_seconds != 0 and len(
                power_ups) == 0:
            power_up = PowerUp(SCREEN, random.randint(1, 3), WIDTH)
            power_ups.append(power_up)

        if len(power_ups) != 0:
            power_ups[0].move()
            if power_ups[0].y_pos + power_ups[0].height > ground:
                power_ups.remove(power_ups[0])
            elif power_up_collected(player, power_ups[0]):
                next((ch for ch in SOUND_CHANNELS if not ch.get_busy()), None).play(POWER_UP_SOUND)
                if power_ups[0].power == 1:
                    player.health += 1
                elif power_ups[0].power == 2:
                    freeze_active = True
                elif power_ups[0].power == 3:
                    auto_fire_active = True

                power_ups.remove(power_ups[0])

        if freeze_active:
            freeze_active = power_up_freeze(spheres, time_played_seconds)

        if auto_fire_active:
            shots, auto_fire_active = power_up_machine_gun(shots, player, tick, time_played_seconds)

        for explosion in EXPLOSIONS:
            if explosion.iteration > 16:
                EXPLOSIONS.remove(explosion)

        # Call to Update Screen
        update_screen(player, shots, spheres, power_ups, game_over)


def power_up_freeze(spheres, game_time):
    duration = 3
    for sphere in spheres:
        if sphere.frozen_time == 0:
            sphere.frozen = True
            sphere.frozen_time = game_time

        elif game_time - sphere.frozen_time >= duration:
            for s in spheres:
                sphere.frozen = False
                s.frozen_time = 0
            return False

    return True


def power_up_machine_gun(shots, player, tick, game_time):
    duration = 3

    if player.machine_gun_active_time == 0:
        player.machine_gun_active_time = game_time

    if tick % 3 == 0:
        auto_shot = Shot(SCREEN, player.aim_point, player.barrel_angle)
        auto_shot.move_shot()
        shots.append(auto_shot)
        next((ch for ch in SOUND_CHANNELS if not ch.get_busy()), None).play(CANNON_SOUND)

    if game_time - player.machine_gun_active_time >= duration:
        player.machine_gun_active_time = 0
        return shots, False

    return shots, True


def power_up_collected(player, power_up):
    if any(power_up.y_pos + i in range(int(player.y_pos), int(player.y_pos) + player.tank_height)
           for i in range(power_up.height)):
        if any(power_up.x_pos + i in range(player.x_pos, player.x_pos + player.tank_width)
               for i in range(power_up.width)):
            return True
    else:
        return False


def sphere_hit(shot, sphere, spheres, player):
    if sphere.gravity == 0:
        sphere.gravity = 3
    # Calculate Shots X and Y Velocities
    shot_x_vel = shot.speed * math.cos(shot.shot_angle)
    shot_y_vel = shot.speed * math.sin(shot.shot_angle)

    # Calculate Angle of Impact
    impact_angle = math.atan2(shot_y_vel, shot_x_vel)

    # Calculate Spheres New Velocity
    new_vel_x = sphere.x_vel + shot.power * math.cos(impact_angle)
    new_vel_y = sphere.y_vel + shot.power * math.sin(impact_angle)

    if new_vel_y > -10:
        new_vel_y = -10

    # Update Spheres Velocities
    sphere.x_vel = new_vel_x
    sphere.y_vel = new_vel_y

    difficulty_curve(new_vel_y, spheres, sphere)

    sphere.times_hit += 1

    if sphere.times_hit == 5 and len(spheres) > 1:
        player.score += 1
        explosion = Explosion(SCREEN, sphere.x_pos, sphere.y_pos + sphere.radius)
        EXPLOSIONS.append(explosion)
        spheres.remove(sphere)
        next((ch for ch in SOUND_CHANNELS if not ch.get_busy()), None).play(EXPLOSION_SOUND)
        del sphere


def difficulty_curve(vel_y, spheres, sphere):

    if len(spheres) < 4:
        new_sphere = Sphere(SCREEN, WIDTH, sphere.x_pos, sphere.y_pos, random.randint(-5, 5),
                            vel_y + random.randint(-5, 0))
        if sphere.frozen_time != 0:
            new_sphere.frozen_time = sphere.frozen_time

        spheres.append(new_sphere)

    elif len(spheres) >= 4 and random.randint(1, 5) == 1:
        new_sphere = Sphere(SCREEN, WIDTH, sphere.x_pos, sphere.y_pos, random.randint(-5, 5),
                            vel_y + random.randint(-5, 0))
        if sphere.frozen_time != 0:
            new_sphere.frozen_time = sphere.frozen_time

        spheres.append(new_sphere)


def update_screen(player, shots, spheres, power_ups, game_over):
    """Calls all update functions and methods to draw everything to the screen"""
    global SCREEN_SHAKE, DISPLAY_CONTROLS

    if SCREEN_SHAKE == 0:
        SCREEN.blit(BACKGROUND, (0, 0))
    else:
        SCREEN.blit(BACKGROUND, (0, random.randint(2, 4)))
        SCREEN_SHAKE -= 1

    if DISPLAY_CONTROLS and len(shots) == 0:
        image = pygame.image.load('./Assets/controls.png')
        SCREEN.blit(image, (150, 80))
    else:
        DISPLAY_CONTROLS = False

    for explosion in EXPLOSIONS:
        explosion.update()

    for shot in shots:
        shot.update()
    for sphere in spheres:
        sphere.update()

    if len(power_ups) != 0:
        power_ups[0].update()

    player.update()

    if game_over is False:
        pygame.display.update()


def end_screen(player, shots, spheres, power_ups, game_over, ground):
    global DISPLAY_CONTROLS

    while True:
        update_screen(player, shots, spheres, power_ups, game_over)

        image = pygame.image.load('./Assets/game_over.png')
        SCREEN.blit(image, (0, 0))
        image = pygame.transform.scale(pygame.image.load('./Assets/target.png'), (50, 50))
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        SCREEN.blit(surface, (250, 430))
        SCREEN.blit(image, (250, 430))
        SCREEN.blit(surface, (700, 430))
        SCREEN.blit(image, (700, 430))

        pygame.display.update()

        player.aim_point = pygame.mouse.get_pos()
        player.move_barrel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                new_shot = Shot(SCREEN, player.aim_point, player.barrel_angle)
                new_shot.move_shot()
                shots.append(new_shot)
                next((ch for ch in SOUND_CHANNELS if not ch.get_busy()), None).play(CANNON_SOUND)

        for shot in shots:
            shot.move_shot()

        for sphere in spheres:
            sphere.move()

            if sphere.y_pos + sphere.radius > ground:
                spheres.remove(sphere)
                explosion = Explosion(SCREEN, sphere.x_pos, sphere.y_pos + sphere.radius)
                EXPLOSIONS.append(explosion)
                del sphere

        for shot in shots:
            if math.sqrt((275 - shot.end_x_pos) ** 2 + (455 - shot.end_y_pos) ** 2) < 25:
                DISPLAY_CONTROLS = True
                game_loop()
            if math.sqrt((725 - shot.end_x_pos) ** 2 + (455 - shot.end_y_pos) ** 2) < 25:
                return True
        CLOCK.tick(60)


def main():
    pygame.mouse.set_visible(0)
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
