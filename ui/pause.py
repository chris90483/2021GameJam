import sys
from enum import Enum

import pygame

from main.constants import Constant


class PauseMenu:

    class Setting(Enum):
        MusicVolume = "music_volume",
        SfxVolume = "sfx_volume",
        ReturnToGame = "return_to_game"
        QuitGame = "quit_game"

    def __init__(self, audio_manager):
        self.paused = False
        self.audio_manager = audio_manager

        self.settings = [self.Setting.MusicVolume, self.Setting.SfxVolume, self.Setting.ReturnToGame, self.Setting.QuitGame]
        self.current_setting_index = 0

    def handle_input(self, event_key):
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

        if event_key == pygame.K_ESCAPE:
            self.paused = not self.paused
            self.current_setting_index = 0

    def change_current_setting(self, direction):
        if direction == 'down':
            self.current_setting_index = (self.current_setting_index + 1) % len(self.settings)
        else:
            self.current_setting_index = (self.current_setting_index - 1) % len(self.settings)

    def draw(self, window):
        if self.paused is True:
            self.render_pause_screen(window)
            return True
        else:
            return False

    def render_pause_screen(self, window):
        default_gray = (123, 123, 123)
        default_black = (0, 0, 0)

        total_top_offset = 0

        pygame.draw.rect(window, (255, 255, 255), pygame.Rect(Constant.SCREEN_WIDTH / 2 - 400 / 2, Constant.SCREEN_HEIGHT / 4, 400, 250))

        paused_font = pygame.font.SysFont("Arial", 50)
        textsurface = paused_font.render('Game Paused', False, (0, 0, 0))
        window.blit(textsurface,
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

        window.blit(vol_textsurface,
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

        window.blit(sfx_vol_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - sfx_vol_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        return_font = pygame.font.SysFont("Arial", 24)
        if self.settings[self.current_setting_index] == self.Setting.ReturnToGame:
            return_textsurface = return_font.render('Return to Game', False, default_black)
        else:
            return_textsurface = return_font.render('Return to Game', False, default_gray)

        total_top_offset += return_textsurface.get_height()

        window.blit(return_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - return_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))

        exit_font = pygame.font.SysFont("Arial", 24)
        if self.settings[self.current_setting_index] == self.Setting.QuitGame:
            exit_textsurface = exit_font.render('Quit Game', False, default_black)
        else:
            exit_textsurface = exit_font.render('Quit Game', False, default_gray)

        total_top_offset += exit_textsurface.get_height()

        window.blit(exit_textsurface,
                         (Constant.SCREEN_WIDTH / 2 - exit_textsurface.get_width() / 2,
                          Constant.SCREEN_HEIGHT / 4 + total_top_offset))