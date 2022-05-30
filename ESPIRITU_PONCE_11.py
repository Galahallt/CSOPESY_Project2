#!/usr/bin/env python

""" Understanding Process Synchronization

In this project, the task is to create a solution to manage a number of
people inside the fitting room of a department store.
"""

__authors__ = ["Paolo Espiritu", "Andre Ponce"]
__email__ = ["paolo_edni_v_espiritu@dlsu.edu.ph", "andre_ponce@dlsu.edu.ph"]
__date__ = "2022/05/30"
__license__ = "MIT"
__version__ = "1.0"

import threading
import time


def green_enter():
    global threadId, fitting_room
    fitting_room.acquire()
    print(threading.current_thread().name)
    threadId += 1
    time.sleep(1)
    fitting_room.release()


def blue_enter():
    global threadId, fitting_room
    fitting_room.acquire()
    print(threading.current_thread().name)
    threadId += 1
    time.sleep(1)
    fitting_room.release()


if __name__ == "__main__":
    n, b, g = list(
        map(int, input("Enter 3 space-separated integers (n, b, g): ").split())
    )

    # initialize n slots inside fitting room
    global fitting_room
    fitting_room = threading.BoundedSemaphore(value=n)

    # initialize id of thread
    global threadId
    threadId = 0

    print("Blue Only")
    for i in range(b):
        # create blue thread
        blue = threading.Thread(
            target=blue_enter, name="Thread ID: " + str(threadId) + " | Color: Blue"
        )
        # start blue thread
        blue.start()
        time.sleep(1)
    print("Empty Fitting Room")

    print("Green Only")
    for j in range(g):
        # create green thread
        green = threading.Thread(
            target=green_enter, name="Thread ID: " + str(threadId) + " | Color: Green"
        )
        # start green thread
        green.start()
        time.sleep(1)
    print("Empty Fitting Room")
