import pygame

import Block
import Config
import I18n
from Dialog import Dialog
from ui.DialogUI import DialogUI
from ui.TradeUI import TradeUI
from entity.NPC import TraderNPC, TradeOption


class NetherNPC1(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc1'), pos,
                         pygame.transform.scale(pygame.image.load("./assets/trainer.png"), (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc1_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc1_option2'), 0, self.buy_2)
                         ])
        self.traded = False

    @staticmethod
    def buy_1(player, npc, opt):
        Config.CLIENT.dimension.set_block((2, 17), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc1_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        Config.CLIENT.dimension.set_block((3, 19), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc1_option2')))

    def on_interact(self, player):
        if not self.traded:
            Config.CLIENT.open_ui(DialogUI(Dialog('./assets/dialogs/nether_npc1.json'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))


class NetherNPC2(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc2'), pos,
                         pygame.transform.scale(pygame.image.load("./assets/trainer.png"), (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc2_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc2_option2'), 0, self.buy_2)
                         ])
        self.traded = False

    @staticmethod
    def buy_1(player, npc, opt):
        Config.CLIENT.dimension.set_block((7, 11), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc2_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        Config.CLIENT.dimension.set_block((8, 10), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc2_option2')))

    def on_interact(self, player):
        if not self.traded:
            Config.CLIENT.open_ui(DialogUI(Dialog('./assets/dialogs/nether_npc2.json'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))


class NetherNPC3(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc3'), pos,
                         pygame.transform.scale(pygame.image.load("./assets/trainer.png"), (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc3_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc3_option2'), 0, self.buy_2)
                         ])
        self.traded = False

    @staticmethod
    def buy_1(player, npc, opt):
        Config.CLIENT.dimension.set_block((18, 18), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc3_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        Config.CLIENT.dimension.set_block((19, 19), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc3_option2')))

    def on_interact(self, player):
        if not self.traded:
            Config.CLIENT.open_ui(DialogUI(Dialog('./assets/dialogs/nether_npc3.json'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))


class NetherNPC4(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc4'), pos,
                         pygame.transform.scale(pygame.image.load("./assets/trainer.png"), (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc4_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc4_option2'), 0, self.buy_2)
                         ])
        self.traded = False

    @staticmethod
    def buy_1(player, npc, opt):
        # Config.CLIENT.dimension.set_block((7, 11), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc4_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        # Config.CLIENT.dimension.set_block((8, 10), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc4_option2')))

    def on_interact(self, player):
        if not self.traded:
            Config.CLIENT.open_ui(DialogUI(Dialog('./assets/dialogs/nether_npc4.json'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))


class NetherNPC5(TraderNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('nether_npc5'), pos,
                         pygame.transform.scale(pygame.image.load("./assets/trainer.png"), (50, 50)),
                         trade_list=[
                             TradeOption(I18n.text('nether_npc4_option1'), 0, self.buy_1),
                             TradeOption(I18n.text('nether_npc4_option2'), 0, self.buy_2)
                         ])
        self.traded = False

    @staticmethod
    def buy_1(player, npc, opt):
        # Config.CLIENT.dimension.set_block((7, 11), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc5_option1')))

    @staticmethod
    def buy_2(player, npc, opt):
        # Config.CLIENT.dimension.set_block((8, 10), Block.WARPED_PLANKS)
        npc.traded = True
        Config.CLIENT.close_ui()
        return I18n.literal(I18n.text('bought').format(I18n.text('nether_npc5_option2')))

    def on_interact(self, player):
        if not self.traded:
            Config.CLIENT.open_ui(DialogUI(Dialog('./assets/dialogs/nether_npc5.json'),
                                           lambda msg: Config.CLIENT.open_ui(TradeUI(player, self))))
