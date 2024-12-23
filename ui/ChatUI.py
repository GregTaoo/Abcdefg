import time

import pygame

import Config
from ui.UI import UI


class ChatUI(UI):

    def __init__(self):
        super().__init__()
        self.input_rect = pygame.Rect(10, Config.SCREEN_HEIGHT - 40, Config.SCREEN_WIDTH - 20, 30)
        self.text = ''
        self.bg_color = (50, 50, 50)
        self.text_color = (255, 255, 255)

    def get_response(self, text):
        return 'AI: You said: ' + text

    def send_message(self, text):
        response = self.get_response(text)
        Config.CLIENT.current_hud.messages.insert(0, ('You: ' + text, time.time()))
        Config.CLIENT.current_hud.messages.insert(0, (response, time.time()))
        Config.CLIENT.close_ui()

    def tick(self, keys, events):
        super().tick(keys, events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.send_message(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return False
                else:
                    self.text += event.unicode
        return True

    def render(self, screen: pygame.Surface):
        super().render(screen)
        pygame.draw.rect(screen, self.bg_color, self.input_rect)
        txt_surface = Config.FONT.render(self.text, True, self.text_color)
        screen.blit(txt_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        y_offset = Config.SCREEN_HEIGHT - 50
        max_height = 600
        max_width = Config.SCREEN_WIDTH // 2
        messages_to_render = [(msg, ts) for msg, ts in Config.CLIENT.current_hud.messages]

        for message, timestamp in messages_to_render:
            lines = []
            while message:
                for i in range(len(message)):
                    if Config.FONT.size(message[:i])[0] > max_width:
                        break
                else:
                    i = len(message)
                lines.append(message[:i])
                message = message[i:]
            for line in lines:  # Render each line from bottom to top
                txt_surface = Config.FONT.render(line, True, (255, 255, 255))
                y_offset -= txt_surface.get_height() + 5
                if y_offset < Config.SCREEN_HEIGHT - max_height:
                    return
                screen.blit(txt_surface, (10, y_offset))
