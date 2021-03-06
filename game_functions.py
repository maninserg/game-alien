import sys
from time import sleep
import pygame
from alien import Alien
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond for key downs

    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        #Create a new bullet and update group bullets
        if len(bullets) < ai_settings.bullets_allowed:
             new_bullet = Bullet(ai_settings, screen, ship)
             bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """Respond for key ups """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """Process touchs of buttom keyboard and mouse

    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """ Start new game for touch button Play

    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset settings of speed of game
        ai_settings.initialize_dynamic_settings()
        # Don't show a mouse
        pygame.mouse.set_visible(False)
        # Reset game's statics
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Reset list aliens and bullets
        aliens.empty()
        bullets.empty()
        # Create a new flot and ship to the center
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Update positions of bullets and delete bullets than outside screen

    """
    #Update positions of bullets
    bullets.update()
    #Delete bullets than outside screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    """ Check hits to aliens
    Delete bullets and aliens with hit """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
            check_high_score(stats, sb)
    #Create a new fleet of aliens
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    """Calculate the amount of aleins in row

    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Calculate the amount of rows

    """
    available_space_y = (ai_settings.screen_height -
                         10 * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create alien and placement in the row

    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create fleet of aliens

    """
    #Create alien and calculate the amount of aliens in the row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    #Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """React for attaiment of alien to the edge of screen

    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
    """Down all fleet and change direction of fleet

    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Check alien get to the down of the screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #happenes that for hit "alien-ship
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check attaiment fleet to the edge of screen, update all aliens

    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Check collision "aliens-ship"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    #Check aliens get to the down of the screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, bg):
    """Update screen and create a new screen

    """
    #For every step circle it refresh screen

    #screen.fill(ai_settings.bg_color)
    screen.blit(bg, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Show count
    sb.show_score()
    # Button "Play" is showed if game is not active
    if not stats.game_active:
        play_button.draw_button()
    #Show the last screen
    pygame.display.flip()

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Process the hit the ship with the alien """
    if stats.ship_left > 0:
        # Decrease ship_left
        stats.ship_left -= 1

        sb.prep_ships()
        # Clean lists of aliens and bullets
        aliens.empty()
        bullets.empty()
        # Create a new flot of alieans and place the ship to the center of the
        # screen
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
