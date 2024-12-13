from entity import Entity


class NPC(Entity):

    def dialog(self):
        return "私は" + self.name + "です、よろしくお願いします!"
