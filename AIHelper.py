import threading

from openai import OpenAI

CLIENT = None
MESSAGES = [{
    'role': 'system',
    'content': 'You are now a assistant of this game. You must reply within 50 words. '
               'You should help players with their questions about the '
               'game. Player should beat the zombies in the first WORLD,'
               ' and enter the 2nd world to interact with those NPCs,'
               ' and then go back to 1st world and go to the 3rd world to beat the boss.'
}]
EVENTS = []


def init():
    global CLIENT
    CLIENT = OpenAI(
        base_url='http://10.15.88.73:5011/v1',
        api_key='ollama',  # required but ignored
    )


def get_response(input_text, role='user'):
    user = {
        'role': role,
        'content': input_text
    }
    event = {
        'role': 'system',
        'content': ';'.join(EVENTS)
    }
    ret = 'loading' if CLIENT is None else CLIENT.chat.completions.create(messages=MESSAGES + [event, user],
                                                                           model='llama3.2', stream=True)
    MESSAGES.append(user)
    return ret


thread = threading.Thread(target=init)
thread.start()
