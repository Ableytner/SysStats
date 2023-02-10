from threading import Thread
import os

from django.apps import AppConfig

class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self) -> None:
        from stats.stat_getter import _update_func

        # create the images folder if it doesn't exist
        # this folder contains temporary images
        if os.getcwd().rsplit(os.sep, maxsplit=1)[-1] == "sysstats":
            images_path = os.path.join(os.getcwd(), "stats", "static", "images")
        else:
            images_path = os.path.join(os.getcwd(), "sysstats", "stats", "static", "images")

        if not os.path.isdir(images_path):
            print("images folder not found, creating...", end="")
            os.mkdir(images_path)
            print("Done")

        # start the thread that updates the stats every n seconds
        Thread(target=_update_func, daemon=True).start()
