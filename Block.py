from typing import Tuple

import pygame

from render import Animation
from entity import Player
from Config import BLOCK_SIZE


class Block:

    def __init__(self, name: str, image, is_animation=False, obstacle=False):
        self.name = name
        self.image = image
        self.is_animation = is_animation
        self.path = obstacle

    @staticmethod
    def get_rect(block_pos: Tuple[int, int]):
        return pygame.Rect(block_pos, (BLOCK_SIZE, BLOCK_SIZE))

    def on_entity(self, block_pos: Tuple[int, int], mob):
        pass

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]):
        if self.is_animation:
            self.image.render(screen, pos)
        else:
            screen.blit(self.image, pos)


class LavaBlock(Block):

    def on_entity(self, block_pos: Tuple[int, int], mob):
        mob.fire_tick = 450
        overlap = mob.get_rect().clip(self.get_rect(block_pos))
        mob.damage((overlap.width * overlap.height) / BLOCK_SIZE ** 2 / 3)


class WaterBlock(Block):

    def on_entity(self, block_pos: Tuple[int, int], mob):
        mob.fire_tick = 0
        overlap = mob.get_rect().clip(self.get_rect(block_pos))
        mob.cure((overlap.width * overlap.height) / BLOCK_SIZE ** 2 / 5)


class PortalBlock(Block):

    def __init__(self, name: str, image, is_animation=False, obstacle=False, target_dimension=None, target_pos=(0, 0)):
        super().__init__(name, image, is_animation, obstacle)
        self.target_dimension = target_dimension
        self.target_pos = target_pos

    def on_entity(self, block_pos: Tuple[int, int], mob):
        if isinstance(mob, Player.Player):
            mob.teleport(self.target_dimension, self.target_pos)


def create_image(file: str):
    return pygame.transform.scale(pygame.image.load("assets/" + file), (BLOCK_SIZE, BLOCK_SIZE))


GRASS_BLOCK = Block("grass_block", create_image("grass_block.png"))
STONE = Block("stone", create_image("stone.png"), obstacle=True)
LAVA = LavaBlock("lava", Animation.LAVA, True)
WATER = WaterBlock("water", Animation.WATER, True)
NETHER_PORTAL = PortalBlock("nether_portal", Animation.NETHER_PORTAL, True,
                            target_dimension='the_nether', target_pos=(60, 1080))
GRASS_BLOCK_WITH_FLOWER = Block("grass_block_with_flower", create_image("grass_block_with_flower.png"))
GRASS_BLOCK_WITH_MUSHROOM = Block("grass_block_with_mushroom", create_image("grass_block_with_mushroom.png"))
END_PORTAL = PortalBlock("end_portal", Animation.END_PORTAL, True,
                         target_dimension='the_end')
NETHER_BACK_PORTAL = PortalBlock("nether_portal", Animation.NETHER_PORTAL, True,
                                 target_dimension='the_world', target_pos=(1080, 1080))
END_STONE = Block("end_stone", create_image("end_stone.png"))
WARPED_PLANKS = Block("warped_planks", create_image("warped_planks.png"))
NETHERITE_BLOCK = Block("netherite_block", create_image("netherite_block.png"), obstacle=True)
OBSIDIAN = Block("obsidian", create_image("obsidian.png"))
REDSTONE_BLOCK = Block("redstone_block", create_image("redstone_block.png"), obstacle=True)
