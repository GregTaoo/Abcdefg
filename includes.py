WORLDS = []
COIN_IMAGE = None


def get_world(name: str):
    for i in WORLDS:
        if i.name == name:
            return i
    return None
