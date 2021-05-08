import time
from asyncio import PriorityQueue, Queue
from threading import Thread

from audio.audio import SoundEmitter
from entities.zombie_handler import ZombieHandler


class EmitterHandler(object):
    TIME_TILL_EMITTER_REMOVAL = 10.0  # Seconds

    def __init__(self, zombie_handler: ZombieHandler):
        self.active_emitters = PriorityQueue()
        self.new_emitters = PriorityQueue()
        self.running = True
        self.thread = Thread(target=self.handler_thread)
        self.thread.start()
        self.current_emitter = None
        self.zombie_handler = zombie_handler

    def add_emitter(self, emitter: SoundEmitter):
        self.new_emitters.put((time.time(), emitter))

    def handler_thread(self):
        while self.running:
            while not self.new_emitters.empty():
                t, emitter = self.new_emitters.get()
                self.current_emitter = emitter
                # self.active_emitters.put((t, emitter)) TODO: Add emitter removal before enabling this

            zombies = self.zombie_handler.get_zombies()

            for zombie in zombies:
                zombie.hear(self.current_emitter)

            time.sleep(0.1)

    def __del__(self):
        # Stop thread on delete
        self.running = False
        self.thread.join()
