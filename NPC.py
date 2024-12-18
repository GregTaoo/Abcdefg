import random
from typing import Tuple

import pygame

import UI
import config
import entity
import i18n
from block import Blocks


class NPC(entity.Entity):
    direction = 0
    dialog_timer = 0

    def __init__(self, name: str, pos: Tuple[int, int], image):
        super().__init__(name, pos, image)

    def dialog(self):
        return i18n.text('npc_dialog').format(self.name)

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
        super().__init__(i18n.text('villager'), pos, pygame.transform.scale(pygame.image.load("assets/villager.png"),
                                                                            (50, 50)),
                         trade_list=[
                             TradeOption(i18n.literal("购买"), 10, lambda player, npc, opt: print("购买")),
                             TradeOption(i18n.literal("购买1"), 10, lambda player, npc, opt: print("购买1")),
                             TradeOption(i18n.literal("购买2"), 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    def on_battle(self, player):
        for trade in self.trade_list:
            trade.price *= 2
        iron_golem = entity.Entity(i18n.text('iron_golem'), self.get_right_bottom_pos(),
                                   pygame.transform.scale(pygame.image.load("assets/iron_golem.png"), (50, 50)), atk=8)
        config.CLIENT.spawn_entity(iron_golem)
        config.CLIENT.open_ui(UI.BattleUI(player, iron_golem))


class MedicineTraderNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__(i18n.text('witch'), pos,
                         pygame.transform.scale(pygame.image.load("assets/trainer.png"), (50, 50)),
                         trade_list=[
                             TradeOption(i18n.literal("锻炼"), 10, self.buy_1),
                             TradeOption(i18n.literal("健身"), 10, self.buy_2),
                             TradeOption(i18n.literal("购买2"), 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            return i18n.text('no_enough_coins')
        player.max_hp += 20
        player.coins -= opt.price
        return i18n.literal("效果显著，增加20体力上限")

    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            return i18n.text('no_enough_coins')
        player.max_hp += 50
        player.coins -= opt.price
        return i18n.literal("十分强大的，增加50体力上限")


class WeaponTraderNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__(i18n.text('weapon_trader'), pos,
                         pygame.transform.scale(pygame.image.load("assets/weapon_trader.png"), (50, 50)),
                         trade_list=[
                             TradeOption(i18n.text('charged_fist'), 10, self.buy_1),
                             TradeOption(i18n.text('iron_sword'), 10, self.buy_2),
                             TradeOption(i18n.literal("购买2"), 10, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            return i18n.text('no_enough_coins')
        player.crt += 0.15
        player.coins -= opt.price
        return i18n.literal(i18n.text('bought').format(i18n.text('charged_fist')))

    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            return i18n.text('no_enough_coins')
        player.atk += 0.1
        player.coins -= opt.price
        return i18n.literal(i18n.text('bought').format(i18n.text('iron_sword')))


class NetherNPC1(TraderNPC):

    def __init__(self, pos):
        super().__init__(i18n.text('nether_npc1'), pos,
                         pygame.transform.scale(pygame.image.load("assets/nether_npc1.png"), (50, 50)),
                         trade_list=[
                             TradeOption(i18n.text('charged_fist'), 0, self.buy_1),
                             TradeOption(i18n.text('iron_sword'), 0, self.buy_2),
                             TradeOption(i18n.literal("购买2"), 0, lambda player, npc, opt: print("购买2")),
                         ])
        self.hp = 1145141919810

    @staticmethod
    def buy_1(player, npc, opt):
        config.CLIENT.dimension.replace_block((2, 17), Blocks.WARPED_PLANKS)
        return i18n.literal(i18n.text('bought').format(i18n.text('charged_fist')))

    @staticmethod
    def buy_2(player, npc, opt):
        config.CLIENT.dimension.replace_block((3, 19), Blocks.WARPED_PLANKS)
        return i18n.literal(i18n.text('bought').format(i18n.text('iron_sword')))


class TradeOption:

    def __init__(self, name: i18n.Text, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade
        self.available = True
