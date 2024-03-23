import sys
import pygame

from time import sleep
from alien import Alien
from bullet import Bullet
from game_stats import GameStats
from settings import Settings
from ship import Ship


class AlienInvasion:

    def __init__(self):
        '''initialize game and create game resources'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # full screen 
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Bubu\'s game')
        
        # create an instance to store game statistics
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events() 
            self._update_screen()
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
            self._update_aliens()
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

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()

    def _check_keydown_events(self, event):
        '''respond to key press'''
        if event.key == pygame.K_RIGHT:
            #move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''create a new bullet and add it to the bullets group'''
        new_bullet = Bullet(self)
        if len(self.bullets) < self.settings.bullet_allowed:
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''update position of bullets and get rid of old bullets'''
        #update bullet positions.
        self.bullets.update()

        # get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            print(len(self.bullets))
        
        # check for any bullets that have hit aliens
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _create_fleet(self):
        '''create the fleet of aliens'''
        # make a single alien
        alien = Alien(self)
        alien_width, alien_height =  alien.rect.size
        # this is the group of aliens

        current_x, current_y = alien_width, alien_height
        # row 
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y) 
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

    def _update_aliens(self):
        '''update the positions of the aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        # look for alien-ship collision /init
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_fleet_edges(self):
        '''respond appropiately if any aliens have reached an edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _ship_hit(self):
        # decrement ships_left
        self.stats.ships_left -= 1

        # get rid of any remaining bullets and aliens
        self.bullets.empty()
        self.aliens.empty()

        # create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
       
        # pause
        sleep(0.5)
        

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
