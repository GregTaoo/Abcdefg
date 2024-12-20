from typing import Tuple

import pygame

import I18n
import Config
from UI.UI import UI
from UI.widget.ClassicButton import ClassicButton


class DialogUI(UI):

    def __init__(self, dialogs: list[Tuple[I18n.Text, I18n.Text]], after_dialog):
        super().__init__()
        self.dialogs = dialogs
        self.after_dialog = after_dialog
        self.current_dialog = 0
        self.next_button = ClassicButton(I18n.text('continue'),
                                         (Config.SCREEN_WIDTH // 2 - 150, Config.SCREEN_HEIGHT // 2 + 10),
                                         (300, 50), (255, 255, 255), (0, 0, 0),
                                         self.next_dialog)
        self.add_button(self.next_button)
        self.update_button_text()

    def update_button_text(self):
        if self.current_dialog < len(self.dialogs) and len(self.dialogs[self.current_dialog]) > 1:
            self.next_button.text = self.dialogs[self.current_dialog][1]
        else:
            self.next_button.text = I18n.text('continue')

    def next_dialog(self):
        self.current_dialog += 1
        if self.current_dialog >= len(self.dialogs):
            Config.CLIENT.close_ui()
            self.after_dialog()
        self.update_button_text()

    def render(self, screen: pygame.Surface):
        super().render(screen)
        if self.current_dialog < len(self.dialogs):
            txt_surface = Config.FONT.render(self.dialogs[self.current_dialog][0].get(), True, (255, 255, 255))
            screen.blit(txt_surface, (Config.SCREEN_WIDTH // 2 - txt_surface.get_width() // 2,
                                      Config.SCREEN_HEIGHT // 2 - 75))

    def tick(self, keys, events):
        super().tick(keys, events)
        return True
