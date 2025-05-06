import asyncio
from core.app_state import AppState
import random
from datetime import datetime
import string


def start_background_loop():
    app = AppState()
    loop = asyncio.new_event_loop()
    app.background_loop = loop
    asyncio.set_event_loop(loop)
    loop.run_forever()


def run_async(coro):
    app = AppState()
    while app.background_loop is None:
        pass
    asyncio.run_coroutine_threadsafe(coro, app.background_loop)


def acw(async_func):
    def wrapper(sender, app_data, user_data):
        run_async(async_func(sender, app_data, user_data))
    return wrapper


def generate_filename():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    time_str = datetime.now().strftime("%H%M%S")
    return letters + time_str
