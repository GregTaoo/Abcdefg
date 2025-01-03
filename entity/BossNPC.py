import Block
import Config
import I18n
from Dialog import Dialog
from entity.NPC import NPC
from render import Renderer
from ui.BattleUI import BattleUI
from ui.DialogUI import DialogUI


class BossNPC1(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('baby_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss1'),
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


class BossNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss2'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            if Config.CLIENT.player.hp > Config.CLIENT.player.max_hp / 2:
               Config.CLIENT.player.damage(Config.CLIENT.player.hp - Config.CLIENT.player.max_hp / 2)
            Config.CLIENT.player.max_hp /= 2
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp/2)
        return "!#"


class BossNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('electro_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss3'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '3':
            Config.CLIENT.player.crt_damage *= 2
        elif choice == '4':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        return "!#"


class BossNPC4(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('inferno_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss4'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '3':
            Config.CLIENT.player.atk /= 2
        elif choice == '4':
            Config.CLIENT.player.crt *= 2

        return "!#"


class BossNPC5(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('lava_hound.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss5'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            return 'b1'
        else:
            return '!#'


class BossNPC6(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('super_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss6'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        self.interact = False
        if choice == '1':
            return 'b1'
        else:
            return '!#'


class HerobrineNPC(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('yourself'), pos, Renderer.image_renderer('herobrine.png', (50, 50)))
        self.battle = True

    def on_battle(self, player):
        Config.CLIENT.open_ui(BattleUI(player, self))
