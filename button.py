import pygame

import config


class Button:

    def __init__(self, pos, size, on_click=lambda: None):
        self.on_click = on_click
        self.active = True
        self.hovered = False
        self.mouse_down = False
        self.mouse_timer = 10
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)

    def tick(self, events):
        if not self.active:
            return
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.mouse_down:
            self.mouse_timer = max(0, self.mouse_timer - 1)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hovered:
                    config.SOUNDS['button1'].play()
                    self.mouse_down = True
            elif self.mouse_down and event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_timer == 0:
                    config.SOUNDS['button2'].play()
                self.on_toggle_click()
                self.mouse_down = False
                self.mouse_timer = 10

    def on_toggle_click(self):
        self.on_click()

    def set_active(self, active):
        self.active = active


class ClassicButton(Button):
    def __init__(self, text, pos, size, font, bg_color=(255, 255, 255), text_color=(0, 0, 0), on_click=lambda: None,
                 border_color=(0, 0, 0), hover_bg_color=(50, 50, 50), hover_text_color=(255, 255, 255),
                 inactive_bg_color=(100, 100, 100), inactive_text_color=(50, 50, 50)):
        super().__init__(pos, size, on_click)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.hover_bg_color = hover_bg_color
        self.hover_text_color = hover_text_color
        self.inactive_bg_color = inactive_bg_color
        self.inactive_text_color = inactive_text_color

    def render(self, screen):
        if not self.active:
            bg_color = self.inactive_bg_color
            text_color = self.inactive_text_color
        elif self.hovered or self.mouse_down:
            bg_color = self.hover_bg_color
            text_color = self.hover_text_color
        else:
            bg_color = self.bg_color
            text_color = self.text_color
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, self.border_color, self.rect, width=1, border_radius=8)
        self.render_text(screen, text_color)

    def render_text(self, screen, text_color):
        text_surface = self.font.render(self.text.get(), True, text_color)
        center = (self.rect.center[0] + 1, self.rect.center[1] + 1) if self.mouse_down else self.rect.center
        text_rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, text_rect)


class ImageButton(Button):

    def __init__(self, image: pygame.Surface, pos, on_click=lambda: None):
        super().__init__(pos, image.get_size(), on_click)
        self.image = image

    def render(self, screen):
        if self.hovered or self.mouse_down:
            bg_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 100))
            screen.blit(bg_surface, self.pos)
        screen.blit(self.image, self.pos)


class TradeButton(ClassicButton):

    def __init__(self, text, pos, size, font, trade_option, bg_color=(255, 255, 255), text_color=(0, 0, 0),
                 on_click=lambda: None, border_color=(0, 0, 0), hover_bg_color=(50, 50, 50),
                 hover_text_color=(255, 255, 255), inactive_bg_color=(100, 100, 100), inactive_text_color=(50, 50, 50)):
        super().__init__(text, pos, size, font, bg_color, text_color, on_click, border_color, hover_bg_color,
                         hover_text_color, inactive_bg_color, inactive_text_color)
        self.trade_option = trade_option

    def on_toggle_click(self):
        text = self.on_click() or None
        if text is not None:
            config.CLIENT.open_message_box(text, config.CLIENT.current_ui)
        self.active = self.trade_option.available

    def render_text(self, screen, text_color):
        render_coin = self.trade_option.price > 0
        text_surface = self.font.render(self.text.get(), True, text_color)
        text_rect = text_surface.get_rect(center=(self.rect.center[0], self.rect.center[1]
                                                  - (10 if render_coin else 0)))
        screen.blit(text_surface, text_rect)
        if render_coin:
            text_surface = config.FONT.render(f"x{self.trade_option.price}", True, (255, 175, 45))
            text_rect = text_surface.get_rect(center=(self.rect.center[0] + 12, self.rect.center[1] + 10))
            screen.blit(text_surface, text_rect)
            screen.blit(config.COIN_IMAGE, (self.rect.center[0] - 22, self.rect.center[1]))
