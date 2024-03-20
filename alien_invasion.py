import sys
import pygame

from settings import Settings
from ship import Ship



class AlienInvasion:

    def __init__(self):
        '''initialize game and create game resources'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.ship = Ship(self)

    def run_game(self):
        while True:
            self._check_events() 
            self._update_screen()
            self.ship.update()
            self.clock.tick(60)
            # redraw the screen druing each pass through the loop.
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # make the most recently drawn screen visible
            pygame.display.flip()

    def _check_events(self):
        '''response to keypresses and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
               
    def _update_screen(self):
        '''update images on the screen, and flip to the new screen'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()

    def _check_keydown_events(self, event):
        '''respond to key press'''
        if event.key == pygame.K_RIGHT:
            #move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
