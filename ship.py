import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """Initialition ship in the start position

        """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        #Load image of ship and create rectagle
        self.image = pygame.image.load('images/rocket.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #A new ship will be created in the down edge of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #Save float coordinate center of ship
        self.center = float(self.rect.centerx)
        #Flags moving ship
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        #Update atribut rect of ship from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship in the current position

        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Place the ship to the center of the down part of the screen """
        self.center = self.screen_rect.centerx
