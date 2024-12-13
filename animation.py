import random

import pygame


class Animation:

    def __init__(self, images: list[pygame.Surface], duration: int, is_random=False):
        self.images = images
        self.duration = duration
        self.ticks = 0
        self.index = 0
        self.is_random = is_random

    def tick(self):
        self.ticks += 1
        if self.ticks >= self.duration:
            self.ticks = 0
            if self.is_random:
                self.index = random.randint(0, len(self.images) - 1)
            else:
                self.index = (self.index + 1) % len(self.images)

    def render(self, screen: pygame.Surface, pos: tuple[int, int]):
        screen.blit(self.images[self.index], pos)


def load_images_from_sprite(file, image_size, resize):
    sprite = pygame.image.load(file)
    sheet_width, sheet_height = sprite.get_size()
    images = []

    for y in range(0, sheet_height, image_size[1]):
        image = sprite.subsurface((0, y, image_size[0], image_size[1]))
        images.append(pygame.transform.scale(image, resize))
    return images


class Animations:

    @staticmethod
    def load_lava_images():
        images = load_images_from_sprite("assets/lava.png", (16, 16), (60, 60))
        return images + images[::-1]

    @staticmethod
    def load_water_images():
        images = load_images_from_sprite("assets/water.png", (16, 16), (60, 60))
        return images + images[::-1]

    FIRE = Animation(load_images_from_sprite("assets/fire.png", (16, 16), (50, 50)), 5)
    LAVA = Animation(load_lava_images(), 10)
    WATER = Animation(load_water_images(), 10)


def get_all_animations():
    return [Animations.FIRE, Animations.LAVA, Animations.WATER]



