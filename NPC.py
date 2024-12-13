import random
from typing import Tuple

import pygame

import entity


class NPC(entity.Entity):

    direction = 0
    dialog_timer = 0

    def dialog(self):
        return "私は " + self.name + " です、よろしくお願いします!"

    def tick(self, dimension, player=None):
        super().tick(dimension, player)
        if self.is_nearby(player):
            self.start_dialog(270)
        if self.dialog_timer > 0:
            self.dialog_timer -= 1
        self.move(self.direction, dimension, 1)
        if random.randint(0, 450) == 0:
            if random.randint(0, 5) == 0:
                self.direction = random.randint(1, 4)
            else:
                self.direction = 0

    def start_dialog(self, duration):
        self.dialog_timer = duration

    def render(self, screen: pygame.Surface, camera: Tuple[int, int], font=None):
        super().render(screen, camera)
        self.render_dialog(screen, camera, font)

    def render_dialog(self, screen, camera, font):
        if self.dialog_timer > 0:
            text_surface = font.render(self.dialog(), True, (0, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topleft = (self.x - camera[0] - (text_rect.width - self.size[0]) // 2, self.y - camera[1] - 30)

            pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(14, 14))
            pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(10, 10))
            screen.blit(text_surface, text_rect.topleft)
