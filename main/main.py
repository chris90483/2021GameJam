from enum import Enum

import pygame
import sys
import time

from audio.audio import AudioManager, Songs, SFX

from main.game import Game
from main.constants import Constant
from main.inventory import Inventory


class Main:

    class Setting(Enum):
        MusicVolume = "music_volume",
        SfxVolume = "sfx_volume",
        ReturnToGame = "return_to_game"
        QuitGame = "quit_game"

    def __init__(self):
        self.offset = 0

        # setup stuff
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.window = pygame.display.set_mode((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT), 0, 32)
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.audio_manager = AudioManager()
        self.game = Game('Wilco', Constant.GRID_WIDTH, Constant.GRID_HEIGHT, self.audio_manager)

        self.paused = False

        self.settings = [self.Setting.MusicVolume, self.Setting.SfxVolume, self.Setting.ReturnToGame, self.Setting.QuitGame]
        self.current_setting_index = 0

        self.audio_manager.play_song(song=Songs.ENERGIEK)

    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            # pygame.quit()
            # sys.exit()
            self.paused = not self.paused
            self.current_setting_index = 0
            pass

        if self.game.is_game_over():
            if event_key == pygame.K_RETURN:
                self.game.reset()

        if self.paused:
            if event_key == pygame.K_DOWN or event_key == pygame.K_s:
                self.change_current_setting('down')
            elif event_key == pygame.K_UP or event_key == pygame.K_w:
                self.change_current_setting('up')

            if self.settings[self.current_setting_index] == self.Setting.MusicVolume:
                if event_key == pygame.K_LEFT or event_key == pygame.K_a:
                    self.audio_manager.update_music_audio_level('left')
                elif event_key == pygame.K_RIGHT or event_key == pygame.K_d:
                    self.audio_manager.update_music_audio_level('right')

            if self.settings[self.current_setting_index] == self.Setting.SfxVolume:
                if event_key == pygame.K_LEFT or event_key == pygame.K_a:
                    self.audio_manager.update_sfx_audio_level('left')
                elif event_key == pygame.K_RIGHT or event_key == pygame.K_d:
                    self.audio_manager.update_sfx_audio_level('right')

            if self.settings[self.current_setting_index] == self.Setting.ReturnToGame:
                if event_key == pygame.K_RETURN:
                    self.paused = False

            if self.settings[self.current_setting_index] == self.Setting.QuitGame:
                if event_key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()

    def change_current_setting(self, direction):
        if direction == 'down':
            self.current_setting_index = (self.current_setting_index + 1) % len(self.settings)
        else:
            self.current_setting_index = (self.current_setting_index - 1) % len(self.settings)

    # Handle all pygame events
    def handle_events(self):
        for event in pygame.event.get():
            self.game.handle_input(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self.handle_key_press(event.key)
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
            if event.type == pygame.MOUSEWHEEL:
                if not self.paused:
                    if event.y == -1:
                        self.game.world.inventory.change_current_selected_item("right")
                    elif event.y == 1:
                        self.game.world.inventory.change_current_selected_item("left")
                    else:
                        print("What the frick kinda mousewheel action was that")

    # Do all updates to the game state in this function
    def update_state(self):
        self.window.fill((0, 0, 0))
        self.game.step()

        # call to the game controller drawing method
        self.game.draw(self.window)

    def run(self):
        while True:
            start_time = time.time()

            # handle pygame events from the queue
            self.handle_events()
            # update the state of the game
            if self.game.is_game_over():
                self.render_game_over_screen()
            elif not self.paused:
                self.update_state()
            else:
                self.render_pause_screen()

            # possibly delay program execution to ensure steady frame rate
            running_time = time.time() - start_time
            if running_time < 1 / Constant.FRAME_RATE:
                time.sleep((1 / Constant.FRAME_RATE) - running_time)

            pygame.display.update()

    def render_game_over_screen(self):
        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(Constant.SCREEN_WIDTH / 2 - 400 / 2, Constant.SCREEN_HEIGHT / 4, 400, 250))

        total_top_offset = 40

        game_over_font = pygame.font.SysFont("Arial", 50)
        textsurface = game_over_font.render('Game Over', False, (0, 0, 0))
        self.window.blit(textsurface,
                         (Constant.SCREEN_WIDTH / 2 - textsurface.get_width() / 2, Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        total_top_offset += textsurface.get_height()

        score_font = pygame.font.SysFont("Arial", 24)
        score_textsurface = score_font.render('Final score: {}'.format(self.game.score.get_score()), False, (0, 0, 0))

        total_top_offset += score_textsurface.get_height()

        self.window.blit(score_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - score_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        restart_font = pygame.font.SysFont("Arial", 24)
        restart_textsurface = restart_font.render('Press enter to restart', False, (0, 0, 0))

        total_top_offset += restart_textsurface.get_height() + 15

        self.window.blit(restart_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - restart_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

    def render_pause_screen(self):
        default_gray = (123, 123, 123)
        default_black = (0, 0, 0)

        total_top_offset = 0

        pygame.draw.rect(self.window, (255, 255, 255), pygame.Rect(Constant.SCREEN_WIDTH / 2 - 400 / 2, Constant.SCREEN_HEIGHT / 4, 400, 250))

        paused_font = pygame.font.SysFont("Arial", 50)
        textsurface = paused_font.render('Game Paused', False, (0, 0, 0))
        self.window.blit(textsurface,
                         (Constant.SCREEN_WIDTH / 2 - textsurface.get_width() / 2, Constant.SCREEN_HEIGHT / 4))

        total_top_offset += textsurface.get_height()

        volume_font = pygame.font.SysFont("Arial", 24)
        # print(self.current_setting_index)
        # print(self.settings[self.current_setting_index])
        volume_text = 'Music Volume ' + str(int(self.audio_manager.music_audio_level * 100)) + "%"
        if self.settings[self.current_setting_index] == self.Setting.MusicVolume:
            vol_textsurface = volume_font.render(volume_text, False, default_black)
        else:
            vol_textsurface = volume_font.render(volume_text, False, default_gray)

        total_top_offset += vol_textsurface.get_height()

        self.window.blit(vol_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - vol_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        sfx_volume_font = pygame.font.SysFont("Arial", 24)
        # print(self.current_setting_index)
        # print(self.settings[self.current_setting_index])
        sfx_volume_text = 'SFX Volume ' + str(int(self.audio_manager.sfx_audio_level * 100)) + "%"
        if self.settings[self.current_setting_index] == self.Setting.SfxVolume:
            sfx_vol_textsurface = sfx_volume_font.render(sfx_volume_text, False, default_black)
        else:
            sfx_vol_textsurface = sfx_volume_font.render(sfx_volume_text, False, default_gray)

        total_top_offset += sfx_vol_textsurface.get_height()

        self.window.blit(sfx_vol_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - sfx_vol_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        return_font = pygame.font.SysFont("Arial", 24)
        if self.settings[self.current_setting_index] == self.Setting.ReturnToGame:
            return_textsurface = return_font.render('Return to Game', False, default_black)
        else:
            return_textsurface = return_font.render('Return to Game', False, default_gray)

        total_top_offset += return_textsurface.get_height()

        self.window.blit(return_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - return_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        exit_font = pygame.font.SysFont("Arial", 24)
        if self.settings[self.current_setting_index] == self.Setting.QuitGame:
            exit_textsurface = exit_font.render('Quit Game', False, default_black)
        else:
            exit_textsurface = exit_font.render('Quit Game', False, default_gray)

        total_top_offset += exit_textsurface.get_height()

        self.window.blit(exit_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - exit_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))


if __name__ == '__main__':
    main = Main()
    main.run()
