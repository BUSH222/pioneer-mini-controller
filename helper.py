import asyncio

background_loop = None


def start_background_loop():
    global background_loop
    loop = asyncio.new_event_loop()
    background_loop = loop
    asyncio.set_event_loop(loop)
    loop.run_forever()


def run_async(coro):
    global background_loop
    while background_loop is None:
        pass
    asyncio.run_coroutine_threadsafe(coro, background_loop)


def acw(async_func):
    def wrapper(sender, app_data, user_data):
        run_async(async_func(sender, app_data, user_data))
    return wrapper
