import pygame

from main.constants import Constant


class GameStartMenu:
    def __init__(self, main):
        self.main = main
        self.name = ''

    def draw(self, window):
        if not self.main.game.is_game_started():
            self.render_game_start_screen(window)
            return True
        else:
            return False

    def handle_input(self, event_key):
        if not self.main.game.is_game_started():
            if event_key == pygame.K_RETURN:
                self.main.game.player_name = self.name
                self.main.game.start_game()
            elif pygame.K_a <= event_key <= pygame.K_z:
                self.add_to_name(pygame.key.name(event_key))
            elif event_key == pygame.K_SPACE:
                self.add_to_name(' ')
            elif event_key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]

    def add_to_name(self, string):
        if self.name == '' or self.name[-1:] == ' ':
            self.name += string.upper()
        else:
            self.name += string
        self.name = self.name.replace(' Van ', ' van ').replace(' De ', ' de ').replace(' Der ', ' der ')

    def render_game_start_screen(self, window):
        start_screen_width = Constant.SCREEN_WIDTH * 0.6
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(Constant.SCREEN_WIDTH / 2 - start_screen_width / 2, Constant.SCREEN_HEIGHT / 4, start_screen_width, 250))

        total_top_offset = 20

        game_over_font = pygame.font.SysFont("Arial", 50)
        textsurface = game_over_font.render('Welcome, new deliverer!', False, (0, 0, 0))
        window.blit(textsurface,
                         (Constant.SCREEN_WIDTH / 2 - textsurface.get_width() / 2, Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        total_top_offset += textsurface.get_height()

        name_font = pygame.font.SysFont("Arial", 24)
        name_textsurface = name_font.render('Enter your name:', False, (0, 0, 0))

        total_top_offset += name_textsurface.get_height()

        window.blit(name_textsurface,
                          (Constant.SCREEN_WIDTH / 2 - name_textsurface.get_width() / 2,
                           Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        name_input_textsurface = name_font.render(self.name if self.name else ' ', False, (0, 0, 0))

        total_top_offset += name_input_textsurface.get_height() + 10

        window.blit(name_input_textsurface,
                          (Constant.SCREEN_WIDTH / 2 - name_input_textsurface.get_width() / 2,
                           Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        restart_font = pygame.font.SysFont("Arial", 24)
        restart_textsurface = restart_font.render('Press enter to start', False, (0, 0, 0))

        total_top_offset += restart_textsurface.get_height() + 20

        window.blit(restart_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - restart_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))