import random
from typing import Tuple

import pygame

ANIMATIONS = []


class Renderer:

    def tick(self):
        pass

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        pass

    def get_size(self):
        pass

    def get_rect(self):
        pass


class ImageRenderer(Renderer):

    def __init__(self, image: pygame.Surface):
        self.image = image
        self.image_mirrored = pygame.transform.flip(self.image, True, False)

    def tick(self):
        pass

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        screen.blit(self.image_mirrored if mirror else self.image, pos)

    def get_size(self):
        return self.image.get_size()

    def get_rect(self):
        return self.image.get_rect()


class AnimationRenderer(Renderer):

    def __init__(self, images: list[pygame.Surface], duration: int, is_random=False, repeat=True, register=True):
        if register:
            ANIMATIONS.append(self)
        self.images = images
        self.images_mirrored = [pygame.transform.flip(image, True, False) for image in images]
        self.duration = duration
        self.ticks = 0
        self.index = 0
        self.is_random = is_random
        self.repeat = repeat

    def tick(self):
        self.ticks += 1
        if self.ticks >= self.duration:
            self.ticks = 0
            if self.is_random:
                self.index = random.randint(0, len(self.images) - 1)
            else:
                self.index = min(self.index + 1, len(self.images) - 1)
                if self.repeat:
                    self.index %= len(self.images)

    def is_end(self):
        return self.index == len(self.images) - 1

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        index = 0 if use_default else self.index
        screen.blit(self.images_mirrored[index] if mirror else self.images[index], pos)

    def get_size(self):
        return self.images[0].get_size()

    def get_rect(self):
        return self.images[0].get_rect()


class EntityRenderer(Renderer):

    def __init__(self, images: list[pygame.Surface], images_moving: list[pygame.Surface],
                 duration: int, pos_delta=(0, 0), pos_delta_mirrored=(0, 0), register=True):
        if register:
            ANIMATIONS.append(self)
        self.images = images
        self.images_moving = images_moving
        self.images_mirrored = [pygame.transform.flip(image, True, False) for image in images]
        self.images_moving_mirrored = [pygame.transform.flip(image, True, False) for image in images_moving]
        self.duration = duration
        self.ticks = 0
        self.index = 0
        self.pos_delta = pos_delta
        self.pos_delta_mirrored = pos_delta_mirrored

    def tick(self):
        self.ticks += 1
        if self.ticks >= self.duration:
            self.ticks = 0
            self.index = (self.index + 1) % len(self.images)

    def render(self, screen: pygame.Surface, pos: tuple[int, int], mirror=False, use_default=False):
        if mirror:
            delta = self.pos_delta_mirrored
            if use_default:
                img = self.images_mirrored
            else:
                img = self.images_moving_mirrored
        else:
            delta = self.pos_delta
            if use_default:
                img = self.images
            else:
                img = self.images_moving
        screen.blit(img[self.index], (pos[0] + delta[0], pos[1] + delta[1]))

    def get_size(self):
        return self.images[0].get_size()

    def get_rect(self):
        return self.images[0].get_rect()


def image_renderer(file: str, size: Tuple[int, int]):
    return ImageRenderer(pygame.transform.scale(pygame.image.load("./assets/" + file), size))


def load_images_from_sprite(file, image_size, resize):
    sprite = pygame.image.load(file)
    sheet_width, sheet_height = sprite.get_size()
    images = []

    for y in range(0, sheet_height, image_size[1]):
        image = sprite.subsurface((0, y, image_size[0], image_size[1]))
        images.append(pygame.transform.scale(image, resize))
    return images


def load_lava_images():
    images = load_images_from_sprite("./assets/lava.png", (16, 16), (60, 60))
    return images + images[::-1]


def load_water_images():
    images = load_images_from_sprite("./assets/water.png", (16, 16), (60, 60))
    return images + images[::-1]


FIRE = AnimationRenderer(load_images_from_sprite("./assets/fire.png", (16, 16), (50, 50)), 5)
LAVA = AnimationRenderer(load_lava_images(), 10)
WATER = AnimationRenderer(load_water_images(), 10)
NETHER_PORTAL = AnimationRenderer(load_images_from_sprite("./assets/nether_portal.png", (16, 16), (60, 60)), 5)
END_PORTAL = AnimationRenderer(load_images_from_sprite("./assets/end_portal.png", (16, 16), (60, 60)), 5)
PLAYER = EntityRenderer(load_images_from_sprite("./assets/player.png", (34, 26), (67, 50)),
                        load_images_from_sprite("./assets/player_moving.png", (34, 26), (67, 50)),
                        5, pos_delta=(-16, 0), pos_delta_mirrored=(0, 0))
