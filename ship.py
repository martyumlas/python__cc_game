import pygame


class Ship:

    def __init__(self, ai_game):
        '''initialize the ship and set its starting position'''
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        #movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

        # print(vars(self))
        # print(dir(self))

    def update(self):
        '''update the ship's position based on the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed 
            self.rect.x = self.x
        
    def blitme(self):
        '''draw the ship at its current position'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''center the ship on the screen'''
        self.rect.midbottom = self.screen_rect.middlebottom
        self.x = float(self.rect.x)












