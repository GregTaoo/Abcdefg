import threading
import time

from openai import OpenAI

import Config
import I18n

CLIENT = None
MESSAGES = [{
    'role': 'system',
    'content': Config.AI_PROMPT
}]
EVENTS = []


def init():
    global CLIENT
    CLIENT = OpenAI(
        base_url=Config.AI_URL,
        api_key='ollama',  # required but ignored
    )


def update_ai_response(response: str):
    MESSAGES.append({
        'role': 'assistant',
        'content': response
    })


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
