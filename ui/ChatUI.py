import threading
import time

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
    def get_response(text):
        Config.AI_INPUT_LOCK = True

        def fetch_response():
            print('You: ' + text)
            for chunk in AIHelper.get_response(text):
                response.string += chunk.choices[0].delta.content
            AIHelper.update_ai_response(response.string[response.string.find(': ') + 2:])
            print('AI: ' + response.string[response.string.find(': ') + 2:])

        def update_response():
            while True:
                time.sleep(0.01)
                if not thread.is_alive() and response.is_end():
                    Config.CLIENT.current_hud.messages.insert(1, (I18n.literal(response.get()), (255, 255, 0),
                                                                  time.time()))
                    Config.CLIENT.current_hud.messages.pop(0)
                    break
                if response.count():
                    Config.CLIENT.current_hud.messages.insert(1, (I18n.literal(response.get()), (255, 255, 0),
                                                                  time.time()))
                    response.st = response.cnt + 1
            if response.string.count(str(Config.FLAG)) >= 1:
                Config.CLIENT.current_hud.messages.insert(0, (I18n.text('flag_leaked'), (255, 0, 0), time.time()))
            Config.AI_INPUT_LOCK = False

        response = I18n.ai_text(I18n.text('ai_assistant').get(), '')
        thread = threading.Thread(target=fetch_response)
        thread.start()
        thread1 = threading.Thread(target=update_response)
        thread1.start()
        return response

    def send_message(self, text):
        if text.startswith('/tp'):
            x, y = text.split(' ')[1:]
            Config.CLIENT.player.x = int(x)
            Config.CLIENT.player.y = int(y)
            return

        response = self.get_response(text)
        Config.CLIENT.current_hud.messages.insert(0, (I18n.literal(I18n.text('player_name').get() + ': ' + text),
                                                      (255, 255, 255), time.time()))
        Config.CLIENT.current_hud.messages.insert(0, (response, (255, 255, 0), time.time()))
        Config.CLIENT.close_ui()

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

