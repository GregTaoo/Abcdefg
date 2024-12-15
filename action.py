class Action:

    def __init__(self, name: str, file: str):
        self.name = name
        self.pos = []
        self.ticks = 0
        with open(file, "r") as f:
            s = f.read()
            for line in s.split('\n'):
                if len(line) == 0:
                    continue
                self.pos.append(tuple(map(int, line.split())))

    def tick(self):
        self.ticks = min(self.ticks + 1, len(self.pos) - 1)

    def get_current_pos(self):
        return self.pos[self.ticks]

    def is_end(self):
        return self.ticks == len(self.pos) - 1

    def reset(self):
        self.ticks = 0


class Actions:

    ATTACK_RIGHT = Action("attack_right", "assets/attack_right.txt")
    ATTACK_LEFT = Action("attack_left", "assets/attack_left.txt")
    ATTACK_ULT_RIGHT = Action("attack_ult_right", "assets/attack_ult_right.txt")

