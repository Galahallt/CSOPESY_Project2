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


def change_thread():
    global n, b, g
    global ctr, blueCtr, greenCtr, quantum
    global isBlue

    if blueCtr < b and greenCtr < g:
        # if quantum reached, switch to other color
        if ctr == quantum:
            ctr = 0
            isBlue = not isBlue
            print("------Empty Fitting Room------")
        # else, just increment counter
        else:
            ctr += 1
    elif greenCtr == g and not isBlue:
        ctr = 0
        isBlue = True
        print("------Empty Fitting Room------")
    elif blueCtr == b and isBlue:
        ctr = 0
        isBlue = False
        print("------Empty Fitting Room------")
    else:
        ctr = 1


def green_enter():
    global threadId, fitting_room, greenCtr
    fitting_room.acquire()
    print(threading.current_thread().name)
    threadId += 1
    greenCtr += 1
    print(threading.active_count())
    change_thread()
    time.sleep(0.1)
    fitting_room.release()


def blue_enter():
    global threadId, fitting_room, blueCtr
    fitting_room.acquire()
    print(threading.current_thread().name)
    threadId += 1
    blueCtr += 1
    print(threading.active_count())
    change_thread()
    time.sleep(0.1)
    fitting_room.release()


if __name__ == "__main__":
    global n, b, g
    n, b, g = list(
        map(int, input("Enter 3 space-separated integers (n, b, g): ").split())
    )

    # initialize n slots inside fitting room
    global fitting_room
    fitting_room = threading.BoundedSemaphore(value=n)

    # initialize id of thread
    global threadId
    threadId = 0

    global isBlue
    isBlue = True

    if g < b:
        # print("----------Green Only----------")
        isBlue = False
    # else:
    # print("----------Blue Only----------")

    global ctr, blueCtr, greenCtr, quantum
    ctr = blueCtr = greenCtr = 0
    quantum = n + 2

    for i in range(b + g):
        if isBlue:
            if ctr == 0:
                print("----------Blue Only----------")

            # create blue thread
            blue = threading.Thread(
                target=blue_enter, name="Thread ID: " + str(threadId) + " | Color: Blue"
            )
            # start blue thread
            blue.start()
            blue.join()
        else:
            if ctr == 0:
                print("----------Green Only----------")

            # create green thread
            green = threading.Thread(
                target=green_enter,
                name="Thread ID: " + str(threadId) + " | Color: Green",
            )
            # start green thread
            green.start()
            green.join()
