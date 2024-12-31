import threading
import time

import openai
from openai import OpenAI

import Config
import I18n

CLIENT = None
MESSAGES = [{
    'role': 'system',  # 系统消息，初始化为配置的AI提示
    'content': Config.AI_PROMPT
}]
EVENTS = []  # 存储事件的列表


# 向EVENTS列表中添加新事件
def add_event(event: str):
    EVENTS.append(event)
    print(event)

# 初始化AI客户端
def init():
    global CLIENT
    CLIENT = OpenAI(
        base_url=Config.AI_URL,  # 设置AI服务的URL
        api_key='ollama',  # API密钥（在此为假设值）
    )


def update_ai_response(response: str):
    MESSAGES.append({
        'role': 'assistant',
        'content': response
    })


def get_response_stream(input_text, role='user'):
    user = {
        'role': role,
        'content': input_text
    }
    event = {
        'role': 'system',
        'content': ';'.join(EVENTS)
    }
    try:
        ret = None if CLIENT is None else CLIENT.chat.completions.create(messages=MESSAGES + [event, user],
                                                                         model='llama3.2', stream=True, timeout=30)
    except openai.BadRequestError as e:
        print(e)
        ret = None
    MESSAGES.append(user)
    return ret


LOCK = threading.Lock()
LOCK1 = threading.Lock()


def add_response(text, color=(255, 255, 0), role='user'):

    def fetch_response():
        LOCK.acquire()
        LOCK1.acquire()
        LOCK1.release()
        thread1 = threading.Thread(target=update_response)
        thread1.start()
        try:
            Config.AI_INPUT_LOCK = True
            print('You: ' + text)
            stream = get_response_stream(text, role)
            if stream is None:
                response.string += 'ERROR'
                return
            for chunk in stream:
                response.string += chunk.choices[0].delta.content
            update_ai_response(response.string[response.string.find(': ') + 2:])
            print('AI: ' + response.string[response.string.find(': ') + 2:])
        finally:
            LOCK.release()

    def update_response():
        LOCK1.acquire()
        try:
            Config.CLIENT.current_hud.add_message(response, color)
            while True:
                time.sleep(0.01)
                if Config.AI_INPUT_LOCK:
                    if not thread0.is_alive() and response.is_end():
                        Config.CLIENT.current_hud.messages.insert(1, (I18n.literal(response.get()), color,
                                                                      time.time()))
                        Config.CLIENT.current_hud.messages.pop(0)
                        break
                    if response.count():
                        Config.CLIENT.current_hud.messages.insert(1, (I18n.literal(response.get()), color,
                                                                      time.time()))
                        response.st = response.cnt + 1
            if response.string.count(str(Config.FLAG)) >= 1:
                Config.CLIENT.current_hud.messages.insert(0, (I18n.text('flag_leaked'), (255, 0, 0), time.time()))
                Config.NETHER_PORTAL_LOCK = False
            Config.AI_INPUT_LOCK = False
        except AttributeError:
            LOCK1.release()
        finally:
            LOCK1.release()

    response = I18n.ai_text(I18n.text('ai_assistant').get(), '')
    thread0 = threading.Thread(target=fetch_response)
    thread0.start()
    return response


thread = threading.Thread(target=init)
thread.start()
