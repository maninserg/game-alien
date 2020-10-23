import sys

import pygame

def run_game():
    """Initialization game and create screen

    """

    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Alien Invasion")

    while True:
        """Look events keyboard and mouse

        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pygame.display.flip()

run_game()

