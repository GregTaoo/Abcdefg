import random
import sys
import os

import pygame

import AIHelper
import Config
import I18n
import Block
from entity.NPC import VillagerNPC
from entity.NPC import MedicineTraderNPC
from entity.NPC import WeaponTraderNPC
import Client
from Config import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT, BLOCK_SIZE
from entity.Entity import Monster
from entity.Player import Player
from render import Renderer
from render.Renderer import ImageRenderer
from ui.StarterUI import StarterUI


def main():
    os.environ["SDL_IME_SHOW_UI"] = "1"

    print('=================================================================')
    print('Thanks for playing Redemption！')
    print('=================================================================')

    pygame.init()
    pygame.display.set_caption("Redemption")
    pygame.display.set_icon(Block.GRASS_BLOCK.renderer.image)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.scrap.init()
    pygame.key.stop_text_input()

    player = Player(I18n.text('player_name'), (600, 600), (600, 600), Renderer.PLAYER, size=(50, 50))

    Config.CLIENT = Client.Client(screen, clock, player, 'the_world')
    Config.CLIENT.open_ui(StarterUI())

    Config.CLIENT.spawn_entity(VillagerNPC((300, 300)))
    Config.CLIENT.spawn_entity(MedicineTraderNPC((200, 200)))
    Config.CLIENT.spawn_entity(WeaponTraderNPC((400, 400)))

    for _ in range(20):
        Config.CLIENT.spawn_entity(
            Monster(I18n.text('zombie'), (random.randint(0, MAP_WIDTH * BLOCK_SIZE),
                                          random.randint(0, MAP_HEIGHT * BLOCK_SIZE)),
                    ImageRenderer(pygame.transform.scale(pygame.image.load("assets/zombie.png"), (50, 50))), coins=10)
        )

    while True:
        # st = time.time()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                AIHelper.thread.join()
                sys.exit()

        Config.CLIENT.tick(events)

        # 执行渲染
        pygame.display.flip()
        # print(time.time() - st)

        clock.tick(90)


if __name__ == "__main__":
    main()
