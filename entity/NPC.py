from typing import Tuple

import pygame

import AIHelper
import Config
import I18n
from render import Renderer
from ui.BattleUI import BattleUI
from ui.TradeUI import TradeUI
from entity import Entity


class NPC(Entity.Entity):

    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer):
        super().__init__(name, pos, renderer)
        self.dialog_timer = 0
        self.hp = self.max_hp = 11451419198101212
        self.battle = False
        self.interact = True

    def dialog(self):
        return I18n.text('npc_dialog').format(self.name)

    def tick(self, dimension, player=None):
        super().tick(dimension, player)
        if self.is_nearby(player, 2):
            self.start_dialog(270)
        if self.dialog_timer > 0:
            self.dialog_timer -= 1

    def start_dialog(self, duration):
        self.dialog_timer = duration

    def render(self, screen: pygame.Surface, camera: Tuple[int, int]):
        super().render(screen, camera)
        self.render_dialog(screen, camera)

    def render_dialog(self, screen, camera):
        if self.dialog_timer > 0:
            Entity.render_dialog_at_absolute_pos(self.dialog(), screen, (self.x - camera[0] + self.size[0] // 2,
                                                                         self.y - camera[1] - 40), Config.FONT)

    def on_battle(self, player):
        pass


class TraderNPC(NPC):

    def __init__(self, name: str, pos: Tuple[int, int], renderer: Renderer, trade_list=None):
        super().__init__(name, pos, renderer)
        self.trade_list = trade_list if trade_list is not None else []

    def on_interact(self, player):
        AIHelper.add_event(f'player interacted with {self.name}')
        Config.CLIENT.open_ui(TradeUI(player, self))


class VillagerNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('villager'), pos, Renderer.image_renderer('villager.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.literal("购买"), 999, lambda player, npc, opt: print("购买")),
                             TradeOption(I18n.literal("购买1"), 1099, lambda player, npc, opt: print("购买1")),
                             TradeOption(I18n.literal("购买2"), 1990, lambda player, npc, opt: print("购买2")),
                         ])
        self.battle = True

    def on_battle(self, player):
        for trade in self.trade_list:
            trade.price *= 2
        iron_golem = Entity.Entity(I18n.text('iron_golem'), self.get_right_bottom_pos(),
                                   Renderer.image_renderer('iron_golem.png', (50, 50)),
                                   atk=8)
        Config.CLIENT.spawn_entity(iron_golem)
        Config.CLIENT.open_ui(BattleUI(player, iron_golem))


class MedicineTraderNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('witch'), pos, Renderer.image_renderer('witch.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.literal("锻炼"), 10, self.buy_1),
                             TradeOption(I18n.literal("健身"), 10, self.buy_2),
                             TradeOption(I18n.literal("test"), 10, lambda player, npc, opt: print("购买2")),
                         ])

    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')
        player.max_hp += 20
        player.coins -= opt.price
        return I18n.literal("效果显著，增加20体力上限")

    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')
        player.max_hp += 50
        player.coins -= opt.price
        return I18n.literal("十分强大的，增加50体力上限")


class WeaponTraderNPC(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('weapon_trader'), pos, Renderer.image_renderer('weapon_trader.png', (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('charged_fist'), 10, self.buy_1),
                             TradeOption(I18n.text('iron_sword'), 10, self.buy_2),
                             TradeOption(I18n.text("infinite_sword"), 10, self.buy_3),
                         ])

    @staticmethod
    def buy_1(player, npc, opt):
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')
        player.crt += 0.15
        player.coins -= opt.price
        return I18n.literal(I18n.text('bought').format(I18n.text('charged_fist')))

    @staticmethod
    def buy_2(player, npc, opt):
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')
        player.atk += 0.1
        player.coins -= opt.price
        return I18n.literal(I18n.text('bought').format(I18n.text('iron_sword')))
    
    @staticmethod
    def buy_3(player, npc, opt):
        if player.coins < opt.price:
            return I18n.text('no_enough_coins')
        if player.iron < 1:
            return I18n.text("no_iron")
        player.crt_damage += 0.25
        player.coins -= opt.price
        return I18n.literal(I18n.text('bought').format(I18n.text('infinite_sword')))

class TradeOption:

    def __init__(self, name: I18n.Text, price: int, on_trade):
        self.name = name
        self.price = price
        self.on_trade = on_trade
        self.available = True

