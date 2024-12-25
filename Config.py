SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MAP_WIDTH, MAP_HEIGHT = 60, 60
BLOCK_SIZE = 60
INTERACTION_DISTANCE = 1.5

COIN_IMAGE = None
LANGUAGE_IMAGE = None

WORLDS = {}
CLIENT = None
FONT = None
FONT_BOLD = None
MIDDLE_FONT = None
LARGE_FONT = None
HUGE_FONT = None
SOUNDS = {}
CLOCKS = []

AI_URL = 'http://10.15.88.73:5011/v1'
AI_PROMPT = ('You are now a assistant of this game. You must reply within 50 words. '
             'You should help players with their questions about the '
             'game. Player should beat the zombies in the first WORLD,'
             ' and enter the 2nd world to interact with those NPCs,'
             ' and then go back to 1st world and go to the 3rd world to beat the boss.')
