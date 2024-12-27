import Block
import Config
import I18n
from Dialog import Dialog
from entity.NPC import TraderNPC, TradeOption, NPC
from render import Renderer
from ui.DialogUI import DialogUI
from ui.TradeUI import TradeUI

class BossNPC(NPC):
    
    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('trainer.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss_npc'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.dimension.set_block((2, 17), Block.WARPED_PLANKS)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((3, 19), Block.WARPED_PLANKS)
            return 'b2'
        else:
            return '!#'
        
class TrueBossNPC(BossNPC):

    def __init__(self, pos):
        super().__init__(I18n.text('true_boss_npc'), pos, Renderer.image_renderer('trainer.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('true_boss_npc'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.dimension.set_block((2, 17), Block.WARPED_PLANKS)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((3, 19), Block.WARPED_PLANKS)
            return 'b2'
        else:
            return '!#'
        
class FalseBossNPC(BossNPC):

    def __init__(self, pos):
        super().__init__(pos)
        
    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.dimension.set_block((2, 17), Block.WARPED_PLANKS)
            return 'b1'
        elif choice == '2':
            Config.CLIENT.dimension.set_block((3, 19), Block.WARPED_PLANKS)
            return 'b2'
        else:
            return '!#'
        