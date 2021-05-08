import pygame
import sys
import time

from main.game import Game

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAME_RATE = 60
offset = 0

# setup stuff
pygame.init()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)
msg_surface = None
game = Game()

# Do all necessary setup
def setup():
    global msg_surface
    msg_surface = font.render("it works!", False, (255, 255, 255))



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

    object_width = msg_surface.get_width()
    o1 = (offset + 1) % SCREEN_WIDTH
    o2 = (offset + 1 + object_width) % SCREEN_WIDTH
    offset = o1
    if o2 != (o1 + msg_surface.get_width()):
        print(o2-o1 - object_width)
        window.blit(msg_surface, (o2 - object_width, 0))

    window.blit(msg_surface, (offset, 0))

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
        if running_time < 1/FRAME_RATE:
            time.sleep((1/FRAME_RATE) - running_time)

        pygame.display.update()
