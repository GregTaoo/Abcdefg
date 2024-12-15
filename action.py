class Action:

    def __init__(self, name: str, file, get_damage=lambda: 10):
        self.name = name
        self.pos = []
        self.ticks = 0
        self.get_damage = get_damage
        if file is not None:
            with open(file, "r") as f:
                s = f.read()
                for line in s.split('\n'):
                    if len(line) == 0:
                        continue
                    self.pos.append(tuple(map(int, line.split())))

    def tick(self):
        self.ticks = min(self.ticks + 1, len(self.pos) - 1)

    def get_current_pos(self):
        return self.pos[self.ticks] if len(self.pos) > 0 else None

    def is_end(self):
        return self.ticks == len(self.pos) - 1

    def reset(self):
        self.ticks = 0


class Actions:

    ATTACK_RIGHT = Action("attack_right", "assets/attack_right.txt")
    ATTACK_LEFT = Action("attack_left", "assets/attack_left.txt")
    ULTIMATE_RIGHT = Action("ultimate_right", "assets/ultimate_right.txt", lambda: 50)
    ESCAPE_LEFT = Action("escape_left", "assets/escape_left.txt", lambda: 0)
    EMPTY = Action("empty", None, lambda: 0)

