import time
from queue import PriorityQueue, Queue
from threading import Thread

from audio.audio import SoundEmitter
from entities.zombie_handler import ZombieHandler


class EmitterHandler(object):
    TIME_TILL_EMITTER_REMOVAL = 10.0  # Seconds

    def __init__(self, zombie_handler: ZombieHandler):
        self.active_emitters = PriorityQueue()
        self.new_emitters = PriorityQueue()
        self.running = True
        self.current_emitter = None
        self.zombie_handler = zombie_handler
        self.thread = Thread(target=self.handler_thread)
        self.thread.start()

    def add_emitter(self, emitter: SoundEmitter):
        self.current_emitter = emitter

    def handler_thread(self):
        while self.running:
            zombies = self.zombie_handler.get_zombies()

            if self.current_emitter is not None:
                for zombie in zombies:
                    zombie.hear(self.current_emitter)

            time.sleep(0.1)

    def step(self):
        if self.current_emitter is not None:
            delete_emitter = self.current_emitter.step()
            if delete_emitter:
                self.current_emitter = None

    def draw(self, screen, camera):
        if self.current_emitter is not None:
            self.current_emitter.draw(screen, camera)

    def __del__(self):
        # Stop thread on delete
        self.running = False
        self.thread.join()
