import random
from typing import Tuple

import pygame

import entity
import includes


class NPC(entity.Entity):
    direction = 0
    dialog_timer = 0

    def __init__(self, name: str, pos: Tuple[int, int], image, trade_list=None):
        super().__init__(name, pos, image)
        self.trade_list = trade_list if trade_list is not None else []

    def dialog(self):
        return "Hi! My name is " + self.name

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

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        super().render(screen, camera)
        self.render_dialog(screen, camera)

    def render_dialog(self, screen, camera):
        if self.dialog_timer > 0:
            entity.render_dialog_at_absolute_pos(self.dialog(), screen, (self.x - camera[0] + self.size[0] // 2,
                                                                         self.y - camera[1] - 40), includes.FONT)


class VillagerNPC(NPC):

    def __init__(self, pos):
        super().__init__("刁民", pos, pygame.transform.scale(pygame.image.load("assets/villager.png"), (50, 50)),
                         trade_list=[
                             TradeOption("购买", 10, lambda: print("购买")),
                             TradeOption("购买1", 10, lambda: print("购买1")),
                             TradeOption("购买2", 10, lambda: print("购买2")),
                         ])
        self.hp = 1145141919810

class TraderNPC(NPC):

    def __init__(self, pos):
        super().__init__("奸商", pos, pygame.transform.scale(pygame.image.load("assets/trader.png"), (50, 50)),
                         trade_list=[
                             TradeOption("购买", 10, lambda: print("购买")),
                             TradeOption("购买1", 10, lambda: print("购买1")),
                             TradeOption("购买2", 10, lambda: print("购买2")),
                         ])
        self.hp = 1145141919810
        
class TradeOption:

    def __init__(self, name: str, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade
