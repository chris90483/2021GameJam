import pygame
from pygame.event import EventType
from main.constants import Constant
from math import atan2, pi


class DeliveryStatus(object):
    def __init__(self, destination):
        self.destination = destination

    def draw(self, screen: pygame.Surface):
        progress = self.destination.get_delivery_progress()
        if progress > 0:
            progress_bar_width = 200
            pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(50, Constant.SCREEN_HEIGHT - 75, progress_bar_width, 25))
            pygame.draw.rect(screen, (206, 83, 72), pygame.Rect(50, Constant.SCREEN_HEIGHT - 75, progress_bar_width * progress, 25))
