import pygame

from main.constants import Constant


class DeliveryStatus(object):
    def __init__(self, destination, score):
        self.destination = destination
        self.score = score
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen: pygame.Surface):
        progress = self.destination.get_delivery_progress()
        if progress > 0:
            progress_bar_width = 200
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(50, Constant.SCREEN_HEIGHT - 100, progress_bar_width, 25))
            pygame.draw.rect(screen, (253, 127, 0), pygame.Rect(50, Constant.SCREEN_HEIGHT - 100, progress_bar_width * progress, 25))

        progress = self.destination.get_finishing_delivery_progress()
        if progress > 0:
            progress_bar_width = 200
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(50, Constant.SCREEN_HEIGHT - 150, progress_bar_width, 25))
            pygame.draw.rect(screen, (206, 83, 72), pygame.Rect(50, Constant.SCREEN_HEIGHT - 150, progress_bar_width * progress, 25))

        text_surface = self.font.render('Score: {}'.format(self.score.get_score()), True, (255, 255, 255))
        screen.blit(text_surface, (50, Constant.SCREEN_HEIGHT - text_surface.get_height() // 2 - 50))
