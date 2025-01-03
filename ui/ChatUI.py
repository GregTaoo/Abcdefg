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
        # 发送消息的静态方法
        if text.startswith('/tp'):  # 如果消息以 '/tp' 开头，表示传送命令
            x, y = text.split(' ')[1:]  # 获取目标位置坐标
            Config.CLIENT.player.x = int(x)  # 设置玩家的x坐标
            Config.CLIENT.player.y = int(y)  # 设置玩家的y坐标
            return  # 执行完传送后直接返回

        # 普通消息发送
        s = I18n.text('player_name').get() + ': ' + text  # 将玩家名字和消息拼接
        while s:
            i = 0
            # 将消息按屏幕宽度分割，避免文字溢出
            for i in range(len(s)):
                if Config.FONT.size(s[:i + 1])[0] > Config.SCREEN_WIDTH // 2:
                    break
            Config.CLIENT.current_hud.add_message(I18n.text(s[:i + 1]), (255, 255, 255))  # 添加消息到HUD
            s = s[i + 1:]  # 处理剩余的消息

        AIHelper.add_response(text)  # 记录响应
        Config.CLIENT.close_ui()  # 关闭聊天UI

    def paste_text(self):
        if pygame.scrap.get(pygame.SCRAP_TEXT):
            try:
                self.text += pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8').replace('\0', '')
            except UnicodeDecodeError:
                try:
                    self.text += pygame.scrap.get(pygame.SCRAP_TEXT).decode('gbk').replace('\0', '')
                except UnicodeDecodeError:
                    pass

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

