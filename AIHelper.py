import threading

from openai import OpenAI

CLIENT = None


def init():
    global CLIENT
    CLIENT = OpenAI(
        base_url='http://10.15.88.73:5011/v1',
        api_key='ollama',  # required but ignored
    )
    CLIENT.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'You are now a assistant of this game. '
                           'You should help players with their questions about the'
                           ' game. Player should beat the zombies '
            }
        ],
        model='llama3.2',
    )


def get_response(input_text):
    return 'loading' if CLIENT is None else CLIENT.chat.completions.create(messages=[
        {
            'role': 'user',
            'content': input_text
        },
    ], model='llama3.2', stream=True)


thread = threading.Thread(target=init)
thread.start()
