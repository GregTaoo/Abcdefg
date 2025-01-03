import Block
import Config
import I18n
from Dialog import Dialog
from entity.NPC import TraderNPC, NPC
from render import Renderer
from ui.DialogUI import DialogUI
from ui.TradeUI import TradeUI


class NetherNPC1(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc1'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        # 玩家与NPC交互时触发
        if self.interact:
            # 打开对话框UI，调用process_choice方法处理玩家选择
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc1'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        Config.CLIENT.dimension.set_block((0, 19), Block.NETHERITE_BLOCK)
        if choice == '1':
            Config.CLIENT.dimension.set_block((2, 17), Block.NETHERITE_BLOCK)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((3, 19), Block.NETHERITE_BLOCK)
            return 'b2'
        else:
            return '!#'


class NetherNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc2'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc2'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.dimension.set_block((7, 11), Block.NETHERITE_BLOCK)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((8, 10), Block.NETHERITE_BLOCK)
            return 'b2'
        else:
            return '!#'


class NetherNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc3'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc3'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            self.interact = False
            Config.CLIENT.dimension.set_block((2, 7), Block.LAVA)
            Config.CLIENT.dimension.set_block((9, 17), Block.NETHERITE_BLOCK)
            Config.CLIENT.dimension.set_block((19, 19), Block.OAK_TRAPDOOR)
            player.sp -= 2
            player.atk += 0.2
            player.crt += 0.1 # 获得狂暴战刃
            return 'b1'
        else:
            return '!#'


class NetherNPC4(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc4'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        # 玩家与交易NPC交互时触发，打开对话框UI并显示交易界面
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc4'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))
    
    def process_choice(self, player, choice):
        self.interact = False
        if player.sp < 2:
            Config.CLIENT.dimension.set_block((11, 2), Block.LAVA)
            return 'b3'
        elif choice == '1':
            Config.CLIENT.dimension.set_block((11, 2), Block.LAVA)
            # 以5点灵力换取冰霜冲击
            player.sp -= 2
            player.atk += 0.15
            player.atk += 0.15
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((10, 2), Block.LAVA)
            # 清空你所有的灵力，换取50点攻击力，并直接离开这个世界
            return 'b2'
        else:
            return '!#'


class NetherNPC5(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc5'), pos, Renderer.image_renderer('entities/trainer.png', (50, 50)))

    def on_interact(self, player):
        # 玩家与交易NPC交互时触发，打开对话框UI并显示交易界面
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('nether_npc5'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))
            
    def process_choice(self, player, choice):
        self.interact = False
        if player.sp < 2:
            Config.CLIENT.dimension.set_block((20, 10), Block.LAVA)
            return 'b2'
        elif choice == '1':
            Config.CLIENT.dimension.set_block((20, 10), Block.LAVA)
            # 获得回响之杖
            player.sp -= 2
            player.crt += 0.3
            return 'b1'
        else:
            return '!#'

