import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import main

PATH = "/home/www/uploads"

def on_created(event):
    main.main(f"{PATH}/config.cfg")

if __name__ == "__main__":
    event_handler = FileSystemEventHandler()

    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, PATH, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()