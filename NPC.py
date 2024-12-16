import random
from typing import Tuple

import pygame

import client
import entity


class NPC(entity.Entity):
    direction = 0
    dialog_timer = 0

    def __init__(self, name: str, pos: Tuple[int, int], image, can_respawn=False, respawn_pos=None, trade_list=None):
        super().__init__(name, pos, image)
        self.can_respawn = can_respawn
        self.respawn_pos = pos if respawn_pos is None else respawn_pos
        self.trade_list = trade_list if trade_list is not None else []

    def dialog(self):
        return "Hi! My name is " + self.name

    def tick(self, dimension, player=None):
        if self.hp <= 0 and self in client.CLIENT.dimension.entities:
            if self.can_respawn:
                self.respawn_at_pos(self.respawn_pos)
            else:
                client.CLIENT.dimension.entities.remove(self)
                del self
                return
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
        super().render(screen, camera, font)
        self.render_dialog(screen, camera, font)

    def render_dialog(self, screen, camera, font):
        if self.dialog_timer > 0:
            entity.render_dialog_at_absolute_pos(self.dialog(), screen, (self.x - camera[0] + self.size[0] // 2,
                                                                         self.y - camera[1] - 40), font)


class VillagerNPC(NPC):

    def __init__(self, pos):
        super().__init__("刁民", pos, pygame.transform.scale(pygame.image.load("assets/villager.png"), (50, 50)),
                         can_respawn=True, respawn_pos=pos,
                         trade_list=[
                             TradeOption("购买", 10, lambda: print("购买")),
                             TradeOption("购买1", 10, lambda: print("购买1")),
                             TradeOption("购买2", 10, lambda: print("购买2")),
                         ])


class TradeOption:

    def __init__(self, name: str, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade
