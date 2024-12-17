import random
from typing import Tuple

import pygame

import UI
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

    def on_battle(self, player):
        pass


class VillagerNPC(NPC):

    def __init__(self, pos):
        super().__init__("刁民", pos, pygame.transform.scale(pygame.image.load("assets/villager.png"), (50, 50)),
                         trade_list=[
                             TradeOption("购买", 10, lambda player, npc, opt: print("购买")),
                             TradeOption("购买1", 10, lambda player, npc, opt: print("购买1")),
                             TradeOption("购买2", 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    def on_interact(self, player):
        includes.CLIENT.open_ui(UI.TradeUI(player, self))

    def on_battle(self, player):
        for trade in self.trade_list:
            trade.price *= 2
        iron_golem = entity.Entity('Iron Golem', self.get_right_bottom_pos(),
                                   pygame.transform.scale(pygame.image.load("assets/iron_golem.png"), (50, 50)), atk=8)
        includes.CLIENT.spawn_entity(iron_golem)
        includes.CLIENT.open_ui(UI.BattleUI(player, iron_golem))


class Medicine_TraderNPC(NPC):

    def __init__(self, pos):
        super().__init__("女巫", pos, pygame.transform.scale(pygame.image.load("assets/trader.png"), (50, 50)),
                         trade_list=[
                             TradeOption("HP", 10, self.buy_1),
                             TradeOption("购买1", 10, lambda player, npc, opt: print("购买1")),
                             TradeOption("购买2", 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810
    
    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            opt.name = "金币不足"
            return
        opt.name = "购买小型生命药水"
        player.hp = min(player.hp + 20, player.max_hp)
        player.coins -= opt.price
        
    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            opt.name = "金币不足"
            return
        opt.name = "购买中型生命药水"
        player.hp = min(player.hp + 50, player.max_hp)
        player.coins -= opt.price
        
class Weapon_TraderNPC(NPC):

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
            opt.name = "金币不足"
            return
        opt.name = "购买充能拳套"
        player.crt += 15
        player.coins -= opt.price
        
    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            opt.name = "金币不足"
            return
        opt.name = "购买铁剑"
        player.atk += 10
        player.coins -= opt.price

class TradeOption:

    def __init__(self, name: str, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade
