import Config
import I18n
from Dialog import Dialog
from entity.NPC import NPC
from render import Renderer, Action
from ui.BattleUI import BattleUI
from ui.BossBattleUI import BossBattleUI
from ui.DialogUI import DialogUI


class HerobrineNPC(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('yourself'), pos, Renderer.image_renderer('entities/herobrine.png', (50, 50)))
        self.battle = True
        self.actions = [Action.ATTACK_LEFT, Action.LASER_CANNON_LEFT]
        self.hp = 500
        self.max_hp = 500
        self.atk = 10

    def on_battle(self, player):
        Config.CLIENT.open_ui(BossBattleUI(player, self, lambda win: Config.CLIENT.open_ui(DialogUI(
            self, Dialog('boss_true'), lambda msg: self.process_choice(player, msg)))))

    def process_choice(self, player, choice):
        if choice == '1':
            self.hp = 5000 # 脚填数值
            self.max_hp = 5000
            self.atk = 100
            Config.CLIENT.open_ui(BossBattleUI(player, self))
        return "!#"


class BossNPC1(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.GHAST)

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss1'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '3':
            h_npc = HerobrineNPC((500, 500))
            Config.CLIENT.spawn_entity(h_npc)
            Config.CLIENT.open_ui(BattleUI(player, h_npc))
            return "!"
        return "!#"


class BossNPC2(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss2'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            if Config.CLIENT.player.hp > Config.CLIENT.player.max_hp / 2:
                Config.CLIENT.player.damage(Config.CLIENT.player.hp - Config.CLIENT.player.max_hp / 2)
            Config.CLIENT.player.max_hp /= 2
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        return "!#"


class BossNPC3(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('electro_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss3'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '3':
            Config.CLIENT.player.crt_damage *= 2
            self.interact = False
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
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '3':
            Config.CLIENT.player.atk /= 2
        elif choice == '4':
            Config.CLIENT.player.crt *= 2
            self.interact = False

        return "!#"


class BossNPC5(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('lava_hound.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss5'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.player.coins += 100
            self.interact = False
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '4':
            Config.CLIENT.player.atk *= 2
            self.interact = False

        return "!#"


class BossNPC6(NPC):

    def __init__(self, pos):
        super().__init__(I18n.text('boss_npc'), pos, Renderer.image_renderer('super_dragon.png', (50, 50)))

    def on_interact(self, player):
        if self.interact:
            Config.CLIENT.open_ui(DialogUI(self, Dialog('boss6'),
                                           lambda msg: self.process_choice(player, msg)))

    def process_choice(self, player, choice):
        if choice == '1':
            Config.CLIENT.player.heal(1)
        elif choice == '2':
            Config.CLIENT.player.coins += 100
            self.interact = False
        elif choice == '3':
            Config.CLIENT.player.damage(Config.CLIENT.player.hp / 2)
        elif choice == '4':
            Config.CLIENT.player.hp *= 2
            Config.CLIENT.player.max_hp *= 2
            self.interact = False

        return "!#"
