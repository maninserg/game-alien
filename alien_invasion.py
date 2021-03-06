import pygame

from pygame.sprite import Group

from settings import Settings

from ship import Ship

from game_stats import GameStats

from button import Button

from scoreboard import Scoreboard

import game_functions as gf

def run_game():
    """Initialization game and create screen

    """

    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((
        ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    bg = pygame.image.load("images/galaxy.png")

    # Create button "Play"
    play_button = Button(ai_settings, screen, "Play")
    # Create game's statistics and Scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    #Create ship
    ship = Ship(ai_settings, screen)
    #Create group of bullets
    bullets = Group()
    #Create alien
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # Start main cycle of program
    while True:
        #Look events of keyboard and mouse
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb,
                              ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens,
                         bullets)
        #For every step refresh screen
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button, bg)

run_game()

