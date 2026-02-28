import sys
import time
import itertools
from threading import Event


def spinner_task(done_event: Event, current_status: list):
    spinner = itertools.cycle(["|", "/", "-", "\\"])

    while not done_event.is_set():
        sys.stdout.write(f"\r{current_status[0]}... {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.2)

    sys.stdout.write("\rProcess completed!\n")
    sys.stdout.flush()