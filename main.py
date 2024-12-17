import random
import sys

import pygame

import includes
from NPC import VillagerNPC
from NPC import Medicine_TraderNPC
from NPC import Weapon_TraderNPC
from block import Blocks
import client
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, BLOCK_SIZE
from entity import Entity
from player import Player


def main():
    pygame.init()
    pygame.display.set_caption("Minecraft (FAKE)")
    pygame.display.set_icon(Blocks.GRASS_BLOCK.image)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    includes.FONT = pygame.font.Font("assets/simhei.ttf", 16)
    includes.MIDDLE_FONT = pygame.font.Font("assets/simhei.ttf", 24)
    includes.LARGE_FONT = pygame.font.Font("assets/simhei.ttf", 32)

    pygame.mixer.init()

    player = Player("Steve", (600, 600), (600, 600),
                    pygame.transform.scale(pygame.image.load("assets/player.png"), (50, 50)))

    includes.CLIENT = client.Client(screen, clock, player, 'the_world')

    includes.CLIENT.spawn_entity(VillagerNPC((300, 300)))
    includes.CLIENT.spawn_entity(Medicine_TraderNPC((200, 200)))
    includes.CLIENT.spawn_entity(Weapon_TraderNPC((400, 400)))

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        includes.CLIENT.tick(events)

        if random.randint(0, 100) == 0 and len(includes.CLIENT.dimension.entities) < 100:
            includes.CLIENT.spawn_entity(
                Entity("丧尸", (random.randint(0, MAP_WIDTH * BLOCK_SIZE), random.randint(0, MAP_HEIGHT * BLOCK_SIZE)),
                       pygame.transform.scale(pygame.image.load("assets/zombie.png"), (50, 50)), coins=10)
            )

        # 执行渲染
        pygame.display.flip()
        clock.tick(90)


if __name__ == "__main__":
    main()
