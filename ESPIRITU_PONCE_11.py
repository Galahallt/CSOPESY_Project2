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
    global fitting_room, green_access, blue_access
    global greenCtr, blueCtr, b, g, quantum

    # wait for blue threads to release the lock for the fitting room
    while True:
        if not blue_access.locked():
            break

    # acquire the access to the fitting room for the green threads
    if not green_access.locked():
        green_access.acquire()
        print("----------Green Only----------")

    if green_access.locked():
        with fitting_room:
            print(threading.current_thread().name)
            greenCtr += 1
            time.sleep(1)

    # if all green threads are finished or the number of green threads
    # reached the quantum that was set, pass the access to blue threads
    if (greenCtr == g or greenCtr % quantum == 0) and green_access.locked():
        print("------Empty Fitting Room------")
        green_access.release()

    while True:
        if (blue_access.locked() and blueCtr < b) or (blueCtr == b and greenCtr == g):
            break


def blue_enter():
    global fitting_room, green_access, blue_access
    global greenCtr, blueCtr, b, g, quantum

    # wait for green threads to release the lock for the fitting room
    while True:
        if not green_access.locked():
            break

    # acquire the access to the fitting room for the blue threads
    if not blue_access.locked():
        blue_access.acquire()
        print("----------Blue Only-----------")

    if blue_access.locked():
        with fitting_room:
            print(threading.current_thread().name)
            blueCtr += 1
            time.sleep(1)

    # if all blue threads are finished or the number of blue threads
    # reached the quantum that was set, pass the access to green threads
    if (blueCtr == b or blueCtr % quantum == 0) and blue_access.locked():
        print("------Empty Fitting Room------")
        blue_access.release()

    while True:
        if (green_access.locked() and blueCtr < b) or (blueCtr == b and greenCtr == g):
            break


n, b, g = list(map(int, input("Enter 3 space-separated integers (n, b, g): ").split()))

# initialize n slots inside fitting room
fitting_room = threading.BoundedSemaphore(value=n)

green_access = threading.Lock()
blue_access = threading.Lock()

quantum = n + 2

greenCtr = blueCtr = 0

threads = []

# run until the number of blue and green threads are reached
for i in range(b + g):
    if i < b:
        blue = threading.Thread(
            target=blue_enter, name="Thread ID: " + str(i) + " | Color: Blue"
        )
        threads.append(blue)
        blue.start()
    else:
        green = threading.Thread(
            target=green_enter, name="Thread ID: " + str(i) + " | Color: Green"
        )
        threads.append(green)
        green.start()
