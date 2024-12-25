import threading

from openai import OpenAI

CLIENT = None


def init():
    global CLIENT
    CLIENT = OpenAI(
        base_url='http://10.15.88.73:5011/v1',
        api_key='ollama',  # required but ignored
    )


def get_response(input_text, role='user'):
    return 'loading' if CLIENT is None else CLIENT.chat.completions.create(messages=[
        {
            'role': 'system',
            'content': 'You are now a assistant of this game. You must reply within 50 words. '
                       'You should help players with their questions about the '
                       'game. Player should beat the zombies '
        },
        {
            'role': role,
            'content': input_text
        },
    ], model='llama3.2', stream=True)


thread = threading.Thread(target=init)
thread.start()
