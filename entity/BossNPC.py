import Block
import Config
import I18n
from Dialog import Dialog
from entity.NPC import TraderNPC, TradeOption, NPC
from render import Renderer
from ui.DialogUI import DialogUI
from ui.TradeUI import TradeUI

class BossNPC1(NPC):
    
    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('baby_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('baby_dragon'),
                                           lambda msg: self.process_choice(player, msg)))
       
class BossNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('dragon'),
                                           lambda msg: self.process_choice(player, msg)))
      
class BossNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('eletro_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('electro_dragon'),
                                           lambda msg: self.process_choice(player, msg)))