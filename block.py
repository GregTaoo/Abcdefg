from typing import Tuple

import pygame

from config import BLOCK_SIZE


class Block:

    def __init__(self, name: str, image: pygame.Surface, obstacle=False):
        self.name = name
        self.image = image
        self.path = obstacle

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]):
        screen.blit(self.image, pos)


class Blocks:

    @staticmethod
    def create_image(file: str):
        return pygame.transform.scale(pygame.image.load("assets/" + file), (BLOCK_SIZE, BLOCK_SIZE))

    GRASS_BLOCK = Block("grass_block", create_image("grass_block.png"))
    LAVA = Block("lava", create_image("lava.png"), True)