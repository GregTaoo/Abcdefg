import json


class Dialog:

    def __init__(self, filename: str):
        self.filename = filename
        self.dialogs = {}
        self.current = None
        self.load()

    def load(self):
        with open(self.filename, 'r') as f:
            data = json.load(f)
            self.dialogs = data['data']
            self.current = self.dialogs[data['start']]

    def get_dialog(self):
        return self.current

    def next(self, choice: int):
        nxt = self.current['player'][choice]['next']
        if nxt[0] == '!':
            return nxt[1:]
        self.current = self.dialogs[nxt]
        return self.current


'''
{
  "start": "d1",
  "data":{
      "d1": {
        "npc": "qwq",
        "player": [
          {
            "str": "qwq",
            "next": "d2"
          },
          {
            "str": "qwq",
            "next": "d3"
          }
        ]
      },
      "d2": {
        "npc": "qwq2",
        "player": [
          {
            "str": "qwq2",
            "next": "d3"
          }
        ]
      },
      "d3": {
        "npc": "qwq3",
        "player": [
          {
            "str": "qwq3",
            "next": "!1"
          }
        ]
      }
  }
}
'''