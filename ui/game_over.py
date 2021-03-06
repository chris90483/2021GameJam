import pygame

from main.constants import Constant


class GameOverMenu:
    def __init__(self, main):
        self.main = main

    def draw(self, window):
        if self.main.game.is_game_over():
            self.render_game_over_screen(window)
            return True
        else:
            return False
                
    def handle_input(self, event_key):
        if self.main.game.is_game_over():
            if event_key == pygame.K_RETURN:
                self.main.reset()

    def render_game_over_screen(self, window):
        if self.main.game.world.inventory.items[0].flamethrower_sound:
            self.main.game.world.inventory.items[0].flamethrower_sound.stop()
            self.main.game.world.inventory.items[0].flamethrower_sound = None

        if self.main.game.world.player.moving_sound:
            self.main.game.world.player.moving_sound.stop()
            self.main.game.world.player.moving_sound = None

        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(Constant.SCREEN_WIDTH / 2 - 400 / 2, Constant.SCREEN_HEIGHT / 4, 400, 250))

        total_top_offset = 40

        game_over_font = pygame.font.SysFont("Arial", 50)
        textsurface = game_over_font.render('Game Over', False, (0, 0, 0))
        window.blit(textsurface,
                         (Constant.SCREEN_WIDTH / 2 - textsurface.get_width() / 2, Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        total_top_offset += textsurface.get_height()

        score_font = pygame.font.SysFont("Arial", 24)
        score_textsurface = score_font.render('Final profit: € {:.2f}'.format(self.main.game.score.get_score()).replace('.', ','), False, (0, 0, 0))

        total_top_offset += score_textsurface.get_height()

        window.blit(score_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - score_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        restart_font = pygame.font.SysFont("Arial", 24)
        restart_textsurface = restart_font.render('Press enter to restart', False, (0, 0, 0))


        total_top_offset += restart_textsurface.get_height() + 15

        window.blit(restart_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - restart_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        url_font = pygame.font.SysFont("Arial", 40)
        url_font_surface = url_font.render('Check out http://gerben-meijer.nl/index2021.php !', False, (255, 255, 255))

        window.blit(url_font_surface, (200, Constant.SCREEN_HEIGHT - 200, 200, 20))