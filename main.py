import pygame
from player import Player
from shots import Shot

# Global Variables
WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


def game_loop():
    running = True
    player = Player(SCREEN, WIDTH, HEIGHT)
    shots = []

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
                player.time_since_last_shot = 10

        # Moves Shots and Deletes them if they are off the screen in the x-axis
        for shot in shots:
            if shot.start_x_pos < 0 or shot.start_x_pos > WIDTH:
                shots.remove(shot)
                del shot

            else:
                shot.move_shot()

        # Call to Update Screen and Sets FPS
        update_screen(player, shots)
        CLOCK.tick(60)


def update_screen(player, shots):
    """Calls all update functions and methods to draw everything to the screen"""
    SCREEN.fill('black')
    player.update()
    for shot in shots:
        shot.update()
    pygame.display.update()


def main():
    pygame.mouse.set_visible(0)
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
