from threading import Thread

from django.apps import AppConfig

class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self) -> None:
        from stats.stat_getter import _update_func

        # start the thread that updates the stats every n seconds
        Thread(target=_update_func, daemon=True).start()
