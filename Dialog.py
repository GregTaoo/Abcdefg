import json


class Dialog:

    def __init__(self, filename: str):
        self.filename = './assets/dialogs/' + filename + '.json'
        self.dialogs = {}
        self.current = None
        self.load()

    def load(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
            self.dialogs = data['data']
            self.current = self.dialogs[data['start']]

    def next(self, choice: int):
        nxt = self.current['player'][choice]['next']
        if nxt[0] == '!':
            return nxt[1:]
        self.current = self.dialogs[nxt]
        return self.current


'''
{
  "start": "1",
  "data": {
    "1": {
      "npc": "nether_npc2_dia1",
      "player": [
        {
          "str": "nether_player2_dia1",
          "next": "2"
        }
      ]
    },
    "2": {
      "npc": "nether_npc2_dia2",
      "player": [
        {
          "str": "nether_player2_dia2",
          "next": "!1"
        }
      ]
    }
  }
}
'''