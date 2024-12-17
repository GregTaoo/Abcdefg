WORLDS = []
CLIENT = None
COIN_IMAGE = None
PARTICLES = []

FONT = None
MIDDLE_FONT = None
LARGE_FONT = None

SOUND_HIT = None
SOUND_PLAYER_DEATH = None
SOUND_ZEUS = None


def get_world(name: str):
    for i in WORLDS:
        if i.name == name:
            return i
    return None
