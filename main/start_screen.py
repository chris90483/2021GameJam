import pygame
import sys

class StartScreen(object):
    def __init__(self, window):
        self.window = window

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEWHEEL:
                return True
        return False

    def go(self):
        self.window.fill((0, 0, 0))
        self.window.blit(pygame.image.load("./resources/png/startscreen/screen1.png"), (0, 0))

        pygame.display.update()
        go_to_next = False
        while not go_to_next:
            go_to_next = self.handle_events()

        self.window.fill((0, 0, 0))
        self.window.blit(pygame.image.load("./resources/png/startscreen/screen2.png"), (0, 0))

        pygame.display.update()
        go_to_next = False
        while not go_to_next:
            go_to_next = self.handle_events()
