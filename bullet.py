import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''a class to manage bullets fired from the ship'''
    def __init__(self, ai_game):
        '''create a bullet object at the ships current position'''
        super().__init__() # parents constructor
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create a bullet rect a (0, 0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height) 
        self.rect.midtop = ai_game.ship.rect.midtop

        # store the bullets
