import time
from queue import PriorityQueue, Queue
from threading import Thread, Lock

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter
from entities.zombie_handler import ZombieHandler
from main.constants import Constant


class EmitterHandler(object):
    TIME_TILL_EMITTER_REMOVAL = 10.0  # Seconds

    def __init__(self, zombie_handler: ZombieHandler):
        self.active_emitters = PriorityQueue()
        self.new_emitters = PriorityQueue()
        self.running = True
        self.current_emitters = set()
        self.zombie_handler = zombie_handler
        self.lock = Lock()
        self.emitter_surface = Surface((Constant.SCREEN_WIDTH, Constant.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.thread = Thread(target=self.handler_thread)
        self.thread.start()

    def add_emitter(self, emitter: SoundEmitter):
        self.lock.acquire()
        self.current_emitters.add(emitter)
        self.lock.release()

    def handler_thread(self):
        while self.running:
            zombies = self.zombie_handler.get_zombies()
            self.lock.acquire()
            for emitter in self.current_emitters:
                for zombie in zombies:
                    zombie.hear(emitter)

            self.lock.release()

            time.sleep(0.1)

    def step(self):
        self.lock.acquire()
        to_delete = set()
        for emitter in self.current_emitters:
            delete_emitter = emitter.step()
            if delete_emitter:
                to_delete.add(emitter)
        self.current_emitters -= to_delete
        self.lock.release()

    def draw(self, screen, camera):
        self.lock.acquire()
        for emitter in self.current_emitters:
            self.emitter_surface.fill((0, 0, 0, 0))
            emitter.draw(self.emitter_surface, camera)
            screen.blit(self.emitter_surface, (0, 0))
        self.lock.release()

    def quit_thread(self):
        # Stop thread on delete
        self.running = False
        self.thread.join()
