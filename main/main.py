from enum import Enum

import pygame
import sys
import time

from audio.audio import AudioManagement, Songs

from main.game import Game
from main.constants import Constant


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
        self.game = Game(Constant.GRID_WIDTH, Constant.GRID_HEIGHT)

        self.audio_management = AudioManagement()

        self.paused = False

        self.settings = [self.Setting.MusicVolume, self.Setting.SfxVolume, self.Setting.ReturnToGame, self.Setting.QuitGame]
        self.current_setting_index = 0

    # Do all necessary setup
    def setup(self):
        self.audio_management.play_song(song=Songs.ENERGIEK)

    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        if event_key == pygame.K_ESCAPE:
            # end the program, close the window
            # pygame.quit()
            # sys.exit()
            self.paused = not self.paused
            self.current_setting_index = 0
            pass

        if self.paused:
            if event_key == pygame.K_DOWN or event_key == pygame.K_s:
                self.change_current_setting('down')
            elif event_key == pygame.K_UP or event_key == pygame.K_w:
                self.change_current_setting('up')

            if self.settings[self.current_setting_index] == self.Setting.MusicVolume:
                if event_key == pygame.K_LEFT or event_key == pygame.K_a:
                    self.audio_management.update_music_audio_level('left')
                elif event_key == pygame.K_RIGHT or event_key == pygame.K_d:
                    self.audio_management.update_music_audio_level('right')

            if self.settings[self.current_setting_index] == self.Setting.SfxVolume:
                if event_key == pygame.K_LEFT or event_key == pygame.K_a:
                    self.audio_management.update_sfx_audio_level('left')
                elif event_key == pygame.K_RIGHT or event_key == pygame.K_d:
                    self.audio_management.update_sfx_audio_level('right')

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

    # Do all updates to the game state in this function
    def update_state(self):
        self.window.fill((0, 128, 0))
        self.game.step()

        # call to the game controller drawing method
        self.game.draw(self.window)

    def run(self):
        self.setup()
        while True:
            start_time = time.time()

            # handle pygame events from the queue
            self.handle_events()
            # update the state of the game
            if not self.paused:
                self.update_state()
            else:
                self.render_pause_screen()

            # possibly delay program execution to ensure steady frame rate
            running_time = time.time() - start_time
            if running_time < 1 / Constant.FRAME_RATE:
                time.sleep((1 / Constant.FRAME_RATE) - running_time)

            pygame.display.update()

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
        volume_text = 'Music Volume ' + str(int(self.audio_management.music_audio_level * 100)) + "%"
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
        sfx_volume_text = 'SFX Volume ' + str(int(self.audio_management.sfx_audio_level * 100)) + "%"
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
