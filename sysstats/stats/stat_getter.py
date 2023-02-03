from datetime import datetime
from time import sleep

import stats.getter_win as getter_win

UPDATE_DELAY = 600 # 10 minutes

def update():
    getter_win.get()

def _update_func() -> None:
    while True:
        start_time = datetime.now()

        update()
        
        sleep(UPDATE_DELAY - (datetime.now() - start_time).seconds)
