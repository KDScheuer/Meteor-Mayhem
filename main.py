import pygame
from player import Player

WIDTH, HEIGHT = 1000, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


def game_loop():
    running = True
    player = Player(SCREEN, WIDTH, HEIGHT)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            player.move(-1)
        if keys_pressed[pygame.K_d]:
            player.move(1)

        update_screen(player)
        CLOCK.tick(30)


def update_screen(player):
    SCREEN.fill('black')
    player.update()
    pygame.display.update()

def main():
    game_loop()
    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
