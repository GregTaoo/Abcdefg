import random
from typing import Tuple

import pygame

import UI
import config
import entity


class NPC(entity.Entity):
    direction = 0
    dialog_timer = 0

    def __init__(self, name: str, pos: Tuple[int, int], image):
        super().__init__(name, pos, image)

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
                                                                         self.y - camera[1] - 40), config.FONT)

    def on_battle(self, player):
        pass


class TraderNPC(NPC):

    def __init__(self, name: str, pos: Tuple[int, int], image, trade_list=None):
        super().__init__(name, pos, image)
        self.trade_list = trade_list if trade_list is not None else []

    def on_interact(self, player):
        config.CLIENT.open_ui(UI.TradeUI(player, self))


class VillagerNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__("刁民", pos, pygame.transform.scale(pygame.image.load("assets/villager.png"), (50, 50)),
                         trade_list=[
                             TradeOption("购买", 10, lambda player, npc, opt: print("购买")),
                             TradeOption("购买1", 10, lambda player, npc, opt: print("购买1")),
                             TradeOption("购买2", 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    def on_battle(self, player):
        for trade in self.trade_list:
            trade.price *= 2
        iron_golem = entity.Entity('Iron Golem', self.get_right_bottom_pos(),
                                   pygame.transform.scale(pygame.image.load("assets/iron_golem.png"), (50, 50)), atk=8)
        config.CLIENT.spawn_entity(iron_golem)
        config.CLIENT.open_ui(UI.BattleUI(player, iron_golem))


class MedicineTraderNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__("女巫", pos, pygame.transform.scale(pygame.image.load("assets/trader.png"), (50, 50)),
                         trade_list=[
                             TradeOption("小型生命药水", 10, self.buy_1),
                             TradeOption("中型生命药水", 10, self.buy_2),
                             TradeOption("购买2", 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            return "金币不足"
        player.hp = min(player.hp + 20, player.max_hp)
        player.coins -= opt.price
        return "购买小型生命药水"

    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            return "金币不足"
        player.hp = min(player.hp + 50, player.max_hp)
        player.coins -= opt.price
        return "购买中型生命药水"


class WeaponTraderNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__("军火贩", pos, pygame.transform.scale(pygame.image.load("assets/trader.png"), (50, 50)),
                         trade_list=[
                             TradeOption("充能拳套", 10, self.buy_1),
                             TradeOption("铁剑", 10, self.buy_2),
                             TradeOption("购买2", 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            return "金币不足"
        player.crt += 0.15
        player.coins -= opt.price
        return "购买了充能拳套"

    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            return "金币不足"
        player.atk += 0.1
        player.coins -= opt.price
        return "购买了铁剑"


class TradeOption:

    def __init__(self, name: str, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade
        self.available = True
