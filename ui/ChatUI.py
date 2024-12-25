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
        def fetch_response():
            for chunk in AIHelper.get_response(text):
                response.string += chunk.choices[0].delta.content
            AIHelper.update_ai_response(response.get())

        def update_response():
            while True:
                time.sleep(0.01)
                if not thread.is_alive() and response.is_end():
                    break
                response.count()

        response = I18n.ai_text(I18n.text('ai_assistant').get() + ': ')
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
        Config.CLIENT.current_hud.messages.insert(0, (I18n.literal('You: ' + text), (255, 255, 255), time.time()))
        Config.CLIENT.current_hud.messages.insert(0, (response, (255, 255, 0), time.time()))
        Config.CLIENT.close_ui()

    def tick(self, keys, events):
        super().tick(keys, events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
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

        y_offset = Config.SCREEN_HEIGHT - 50
        max_height = 600
        max_width = Config.SCREEN_WIDTH // 2
        messages_to_render = [(msg, color, ts) for msg, color, ts in Config.CLIENT.current_hud.messages]

        for message, color, timestamp in messages_to_render:
            lines = []
            message = message.get()
            while message:
                for i in range(len(message)):
                    if Config.FONT.size(message[:i])[0] > max_width or (i > 0 and message[i - 1] == '\n'):
                        break
                else:
                    i = len(message)
                lines.append(message[:i])
                message = message[i:]
            for line in reversed(lines):  # Render each line from bottom to top
                txt_surface = Config.FONT.render(line, True, color)
                y_offset -= txt_surface.get_height() + 5
                if y_offset < Config.SCREEN_HEIGHT - max_height:
                    return
                screen.blit(txt_surface, (10, y_offset))
