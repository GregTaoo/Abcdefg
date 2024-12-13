import sys

import pygame

import animation
from NPC import NPC
import UI
from block import Blocks
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MAP_WIDTH, MAP_HEIGHT
from dimension import Dimension
from player import Player


def main():
    pygame.init()
    pygame.display.set_caption("Minecraft (FAKE)")
    pygame.display.set_icon(Blocks.GRASS_BLOCK.image)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font("assets/simhei.ttf", 16)

    player = Player("Steve", (600, 600),
                    pygame.transform.scale(pygame.image.load("assets/player.png"), (50, 50)))
    dimension = Dimension(MAP_WIDTH, MAP_HEIGHT, Dimension.generate_map(MAP_WIDTH, MAP_HEIGHT, [
        Blocks.GRASS_BLOCK, Blocks.LAVA, Blocks.STONE
    ], [80, 1, 1]))
    entities = [
        NPC("刁民", (500, 500), pygame.transform.scale(pygame.image.load("assets/villager.png"), (50, 50))),
        NPC("丧尸", (700, 700), pygame.transform.scale(pygame.image.load("assets/zombie.png"), (50, 50)))
    ]
    camera = player.get_camera(dimension.get_render_size())
    current_ui = None

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 务必先渲染背景
        screen.fill((50, 50, 50))
        dimension.render(screen, camera)
        for i in entities:
            i.render(screen, camera, font)
        player.render(screen, camera, font)

        if current_ui is None:
            # 玩家移动
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:  # 向上移动
                player.move(4, dimension)
            if keys[pygame.K_s]:  # 向下移动
                player.move(3, dimension)
            if keys[pygame.K_a]:  # 向左移动
                player.move(2, dimension)
            if keys[pygame.K_d]:  # 向右移动
                player.move(1, dimension)
            if keys[pygame.K_f]:
                for i in entities:
                    if i.is_nearby(player):
                        current_ui = UI.InputTextUI()

            # 踩岩浆扣血
            # for k in range(50):
            #     if (dimension.get_block_from_pos((player.x + k, player.y + k)) == Blocks.LAVA or
            #             dimension.get_block_from_pos((player.x + 50 - k, player.y + k)) == Blocks.LAVA):
            #         player.hp -= 1 / 90
            # player.hp = max(0, player.hp)
            player.tick(dimension)
            for i in animation.get_all_animations():
                i.tick()
            for i in entities:
                i.tick(dimension, player)

            # 更新摄像机位置
            camera = player.get_camera(dimension.get_render_size())
        else:
            current_ui.render(screen, font)
            if not current_ui.tick(pygame.key.get_pressed(), events):
                current_ui = None

        # 执行渲染
        pygame.display.flip()
        clock.tick(90)


if __name__ == "__main__":
    main()
