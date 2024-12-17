class Action:

    # 格式:
    def __init__(self, name: str, file):
        self.name = name
        self.pos = []
        self.ticks = 0
        if file is not None:
            with open(file, "r") as f:
                s = f.read()
                for line in s.split('\n'):
                    if len(line) == 0:
                        continue
                    line1 = line.split('|')
                    num = line1[0].split()
                    poses = []
                    for i in range(len(num) // 2):
                        poses.append((float(num[i * 2]), float(num[i * 2 + 1])))
                    if len(line1) >= 4:
                        sounds = line1[3].split()
                    self.pos.append((poses, int(line1[1]) if len(line1) >= 2 else 0,
                                     line1[2] if len(line1) >= 3 else '', sounds if len(line1) >= 4 else []))

    def tick(self):
        self.ticks = min(self.ticks + 1, len(self.pos) - 1)

    def get_current_pos(self):
        return self.pos[self.ticks] if len(self.pos) > 0 else (None, 0, '', [])

    def is_end(self):
        return self.ticks == len(self.pos) - 1

    def reset(self):
        self.ticks = 0


class Actions:

    ATTACK_RIGHT = Action("attack_right", "assets/actions/attack_right.txt")
    ATTACK_LEFT = Action("attack_left", "assets/actions/attack_left.txt")
    ULTIMATE_RIGHT = Action("ultimate_right", "assets/actions/ultimate_right.txt")
    ESCAPE_LEFT = Action("escape_left", "assets/actions/escape_left.txt")
    EMPTY = Action("empty", None)


def get_all_actions():
    return [Actions.ATTACK_RIGHT, Actions.ATTACK_LEFT, Actions.ULTIMATE_RIGHT, Actions.ESCAPE_LEFT, Actions.EMPTY]