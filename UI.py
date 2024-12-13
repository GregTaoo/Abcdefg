import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT


class UI:

    def __init__(self, title: str):
        self.title = title

    def tick(self, keys, events):
        return False

    @staticmethod
    # Copilot 写的
    def blur_background(screen: pygame.Surface):
        surface = pygame.Surface(screen.get_size())
        surface.blit(screen, (0, 0))
        for _ in range(5):  # Adjust the range for more/less blur
            surface = pygame.transform.smoothscale(surface, (surface.get_width() // 2, surface.get_height() // 2))
            surface = pygame.transform.smoothscale(surface, screen.get_size())
        screen.blit(surface, (0, 0))

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        self.blur_background(screen)


class InputTextUI(UI):

    def __init__(self):
        super().__init__('Input Text')
        self.input_box = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200)
        self.text = ''

    def tick(self, keys, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return False
                else:
                    self.text += event.unicode
        return True

    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        super().render(screen, font)
        txt_surface = font.render(self.text, True, (0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), self.input_box)
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
