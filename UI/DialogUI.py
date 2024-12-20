import pygame

import I18n
import Config
from Dialog import Dialog
from UI.UI import UI
from UI.widget.ClassicButton import ClassicButton


class DialogUI(UI):

    def __init__(self, dialogs: Dialog, after_dialog):
        super().__init__()
        self.dialogs = dialogs
        self.after_dialog = after_dialog
        self.update_buttons(self.dialogs.current['player'])

    def update_buttons(self, options):
        self.buttons.clear()
        for i, option in enumerate(options):
            self.add_button(ClassicButton(I18n.text(option['str']),
                                          (Config.SCREEN_WIDTH // 2 - 150, Config.SCREEN_HEIGHT // 2 + 10),
                                          (300, 50), (255, 255, 255), (0, 0, 0),
                                          lambda index=i: self.next_dialog(index)))

    def next_dialog(self, choice: int):
        nxt = self.dialogs.next(choice)
        if isinstance(nxt, str):
            self.after_dialog(nxt)
            return
        self.update_buttons(nxt['player'])

    def render(self, screen: pygame.Surface):
        super().render(screen)
        txt_surface = Config.FONT.render(I18n.text(self.dialogs.current['npc']).get(), True, (255, 255, 255))
        screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                  Config.SCREEN_HEIGHT // 2 - 75))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True
