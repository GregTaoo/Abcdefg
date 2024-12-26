import pygame

import AIHelper
import Config
import I18n
from ui.UI import UI


class ChatUI(UI):

    def __init__(self):
        super().__init__()
        self.input_rect = pygame.Rect(10, Config.SCREEN_HEIGHT - 40, Config.SCREEN_WIDTH - 20, 30)
        self.text = ''
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)
        pygame.key.start_text_input()
        pygame.key.set_text_input_rect(self.input_rect)

    def on_close(self):
        pygame.key.stop_text_input()
        super().on_close()

    @staticmethod
    def send_message(text):
        if text.startswith('/tp'):
            x, y = text.split(' ')[1:]
            Config.CLIENT.player.x = int(x)
            Config.CLIENT.player.y = int(y)
            return

        Config.CLIENT.current_hud.add_message(I18n.literal(I18n.text('player_name').get() + ': ' + text),
                                              (255, 255, 255))
        AIHelper.add_response(text)
        Config.CLIENT.close_ui()

    def paste_text(self):
        if pygame.scrap.get(pygame.SCRAP_TEXT):
            self.text += pygame.scrap.get(pygame.SCRAP_TEXT).decode('gbk').replace('\0', '')

    def tick(self, keys, events):
        super().tick(keys, events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if (not Config.AI_INPUT_LOCK) and event.key == pygame.K_RETURN:
                    self.send_message(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_v and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                    self.paste_text()
            if event.type == pygame.TEXTINPUT:
                self.text += event.text
        return True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        pygame.draw.rect(screen, self.bg_color, self.input_rect)
        txt_surface = Config.FONT.render(self.text, True, self.text_color)
        screen.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        y_offset = Config.SCREEN_HEIGHT - 60
        lines_cnt = 0
        for message, color, timestamp in Config.CLIENT.current_hud.messages:
            if len(message.get().strip()) > 0:
                txt_surface = Config.FONT.render(message.get().strip(), True, color)
                screen.blit(txt_surface, (10, y_offset))
                y_offset -= 20
                lines_cnt += 1
            if lines_cnt > 25:
                break

