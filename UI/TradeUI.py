import pygame

import Config
import I18n
from UI.UI import UI
from UI.widget.ClassicButton import ClassicButton
from UI.widget.TradeButton import TradeButton


class TradeUI(UI):

    def __init__(self, player, npc):
        super().__init__()
        self.player = player
        self.buttons = []
        self.npc = npc
        cnt = 0
        for option in npc.trade_list:
            self.add_button(TradeButton(option.name, (Config.SCREEN_WIDTH // 2 - 50, 50 + cnt * 70), (100, 50),
                                        option, (255, 255, 255), (0, 0, 0),
                                        lambda opt=option: self.handle_trade(opt)))
            cnt += 1
        self.add_button(ClassicButton(I18n.text('go_back'),
                                      (Config.SCREEN_WIDTH // 2 - 50, Config.SCREEN_HEIGHT // 2 + 10),
                                      (100, 50), (255, 255, 255), (0, 0, 0),
                                      Config.CLIENT.close_ui))

    def handle_trade(self, option):
        return option.on_trade(self.player, self.npc, option)

    def render(self, screen: pygame.Surface):
        super().render(screen)

    def tick(self, keys, events):
        super().tick(keys, events)
        return True
