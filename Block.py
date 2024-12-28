from typing import Tuple

import pygame

import AIHelper
import Config
import I18n
from Config import BLOCK_SIZE
from entity import Player
from render import Renderer


class Block:

    def __init__(self, name: str, renderer: Renderer, obstacle=False):
        self.name = name
        self.renderer = renderer
        self.path = obstacle

    @staticmethod
    def get_rect(block_pos: Tuple[int, int]):
        return pygame.Rect(block_pos, (BLOCK_SIZE, BLOCK_SIZE))

    def on_entity(self, block_pos: Tuple[int, int], mob):
        pass

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]):
        self.renderer.render(screen, pos, False)


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

    def __init__(self, name: str, renderer, obstacle=False, target_dimension=None, target_pos=(0, 0)):
        super().__init__(name, renderer, obstacle)
        self.target_dimension = target_dimension
        self.target_pos = target_pos

    def on_entity(self, block_pos: Tuple[int, int], mob):
        if isinstance(mob, Player.Player):
            if not Config.NETHER_PORTAL_LOCK:
                mob.teleport(self.target_dimension, self.target_pos)
                AIHelper.add_response(f'player has entered portal and been teleported to {self.target_dimension}')
            else:
                Config.CLIENT.current_hud.hint = I18n.text('nether_portal_lock').get()


def image_renderer(file: str):
    return Renderer.image_renderer(file, (BLOCK_SIZE, BLOCK_SIZE))


GRASS_BLOCK = Block("grass_block", image_renderer("grass_block.png"))
STONE = Block("stone", image_renderer("stone.png"), obstacle=True)
LAVA = LavaBlock("lava", Renderer.LAVA)
WATER = WaterBlock("water", Renderer.WATER)
NETHER_PORTAL = PortalBlock("nether_portal", Renderer.NETHER_PORTAL,
                            target_dimension='the_nether', target_pos=(60, 1080))
GRASS_BLOCK_WITH_FLOWER = Block("grass_block_with_flower", image_renderer("grass_block_with_flower.png"))
GRASS_BLOCK_WITH_MUSHROOM = Block("grass_block_with_mushroom", image_renderer("grass_block_with_mushroom.png"))
END_PORTAL = PortalBlock("end_portal", Renderer.END_PORTAL, target_dimension='the_end')
NETHER_BACK_PORTAL = PortalBlock("nether_portal", Renderer.NETHER_PORTAL,
                                 target_dimension='the_world', target_pos=(1080, 1080))
END_STONE = Block("end_stone", image_renderer("end_stone.png"))
WARPED_PLANKS = Block("warped_planks", image_renderer("warped_planks.png"), obstacle=True)
NETHERITE_BLOCK = Block("netherite_block", image_renderer("netherite_block.png"))
OBSIDIAN = Block("obsidian", image_renderer("obsidian.png"))
OAK_TRAPDOOR = Block("oak_trapdoor", image_renderer("oak_trapdoor.png"), obstacle=True)
REDSTONE_BLOCK = Block("redstone_block", image_renderer("redstone_block.png"), obstacle=True)
