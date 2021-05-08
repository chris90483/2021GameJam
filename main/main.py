import pygame
import sys
import time

from audio.audio import AudioManagement, Songs

from main.game import Game
from main.constants import Constant

offset = 0

# setup stuff
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
window = pygame.display.set_mode((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT), 0, 32)
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)
game = Game(Constant.GRID_WIDTH, Constant.GRID_HEIGHT)


audio_management = AudioManagement()


# Do all necessary setup
def setup():
    audio_management.play_song(song=Songs.ENERGIEK)


# handle a pressed key event in the context of the game root
def handle_key_press(event_key):
    if event_key == pygame.K_ESCAPE:
        # end the program, close the window
        pygame.quit()
        sys.exit()


# Handle all pygame events
def handle_events():
    for event in pygame.event.get():
        game.handle_input(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            handle_key_press(event.key)


# Do all updates to the game state in this function
def update_state():
    global offset, window
    window.fill((0, 128, 0))
    game.step()

    # call to the game controller drawing method
    game.draw(window)


if __name__ == '__main__':
    setup()
    while True:
        start_time = time.time()

        # handle pygame events from the queue
        handle_events()
        # update the state of the game
        update_state()

        # possibly delay program execution to ensure steady frame rate
        running_time = time.time() - start_time
        if running_time < 1/Constant.FRAME_RATE:
            time.sleep((1/Constant.FRAME_RATE) - running_time)

        pygame.display.update()
