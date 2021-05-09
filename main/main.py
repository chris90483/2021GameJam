import sys
import time

import pygame

from audio.audio import AudioManager, Songs
from main.constants import Constant
from main.game import Game
from ui.game_over import GameOverMenu
from ui.game_start import GameStartMenu
from ui.pause import PauseMenu


class Main:

    def __init__(self):
        self.offset = 0

        # setup stuff
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.window = pygame.display.set_mode((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT), 0, 32)
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.audio_manager = AudioManager()
        self.game = Game('<username>', Constant.GRID_WIDTH, Constant.GRID_HEIGHT, self.audio_manager)

        self.pause_menu = PauseMenu(self.audio_manager)
        self.game_over_menu = GameOverMenu(self.game)
        self.game_start_menu = GameStartMenu(self.game)

        self.audio_manager.play_song(song=Songs.ENERGIEK)

    # handle a pressed key event in the context of the game root
    def handle_key_press(self, event_key):
        self.pause_menu.handle_input(event_key)
        self.game_over_menu.handle_input(event_key)
        self.game_start_menu.handle_input(event_key)

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
            if event.type == pygame.MOUSEWHEEL:
                if not self.pause_menu.paused:
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
        # Draw the state once before starting the game so that it is shown as the background of the start menu
        self.update_state()

        while True:
            start_time = time.time()

            # handle pygame events from the queue
            self.handle_events()

            if not self.pause_menu.draw(self.window) and not self.game_over_menu.draw(self.window) and not self.game_start_menu.draw(self.window):
                self.update_state()

            # possibly delay program execution to ensure steady frame rate
            running_time = time.time() - start_time
            if running_time < 1 / Constant.FRAME_RATE:
                time.sleep((1 / Constant.FRAME_RATE) - running_time)

            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
