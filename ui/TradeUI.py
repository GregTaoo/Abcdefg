import pygame

import Config
import I18n
from render import Renderer
from ui.UI import UI
from ui.widget.ClassicButton import ClassicButton
from ui.widget.TradeButton import TradeButton


class TradeUI(UI):

    def __init__(self, player, npc):
        super().__init__()
        self.player = player
        self.buttons = []
        self.npc = npc
        cnt = 0
        for option in npc.trade_list:
            button = TradeButton(option.name, (Config.SCREEN_WIDTH // 2 - 50, 50 + cnt * 70), (100, 50),
                                 option, on_click=lambda opt=option: self.handle_trade(opt))
            if player.coins < option.price:
                button.active = False
            self.add_button(button)
            cnt += 1
        self.add_button(ClassicButton(I18n.text('go_back'),
                                      (Config.SCREEN_WIDTH // 2 - 50, Config.SCREEN_HEIGHT // 2 + 10),
                                      (100, 50), on_click=Config.CLIENT.close_ui))

    def handle_trade(self, option):
        ret = option.on_trade(self.player, self.npc, option)
        for button in self.buttons:
            if isinstance(button, TradeButton):
                button.active = self.player.coins >= button.trade_option.price
        return ret

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.FONT.render(f"{self.player.coins}", True, (255, 175, 45))
        screen.blit(Config.COIN_IMAGE, (10, 10))
        screen.blit(txt_surface, (35, 12))
        Config.CLIENT.player.render_at_absolute_pos(screen, (20, Config.SCREEN_HEIGHT - 70), False, False)
        self.npc.render_at_absolute_pos(screen, (Config.SCREEN_WIDTH - 70, 20), True, False)

    def tick(self, keys, events):
        super().tick(keys, events)
        Renderer.PLAYER.tick()
        return True
