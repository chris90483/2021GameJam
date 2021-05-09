from entities.player import Player
from main.constants import Constant
import pygame


class HealthBar(object):
    def __init__(self, player: Player):
        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.player = player

    def draw(self, screen: pygame.Surface):
        health_bar_width = 200
        health_bar_height = 25
        pygame.draw.rect(screen, (200, 200, 200),
                         pygame.Rect(Constant.SCREEN_WIDTH - (50 + health_bar_width), Constant.SCREEN_HEIGHT - (75 + health_bar_height),
                                     health_bar_width, health_bar_height))
        pygame.draw.rect(screen, (0, 128, 0),
                         pygame.Rect(Constant.SCREEN_WIDTH - (50 + health_bar_width), Constant.SCREEN_HEIGHT - (75 + health_bar_height),
                                     health_bar_width * (self.player.health / 1000.0), health_bar_height))

        text_surface = self.font.render('Health: {}'.format(self.player.health), True, (255, 255, 255))
        screen.blit(text_surface, (Constant.SCREEN_WIDTH - (50 + health_bar_width), Constant.SCREEN_HEIGHT - 60))
