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

from concurrent.futures import thread
import threading
import time


def change_thread():
    global n, b, g
    global ctr, blueCtr, greenCtr, quantum
    global isBlue

    # if there are still green and blue threads to be executed
    if blueCtr < b and greenCtr < g:
        # if quantum reached, switch to other color
        if ctr == quantum:
            ctr = 0
            isBlue = not isBlue
            print("------Empty Fitting Room------")
        # else, just increment counter
        else:
            ctr += 1
    # if there are no more green threads but there are still blue threads to be executed
    elif greenCtr == g and not isBlue:
        ctr = 0
        isBlue = True
        print("------Empty Fitting Room------")
    # if there are no more blue threads but there are still green threads to be executed
    elif blueCtr == b and isBlue:
        ctr = 0
        isBlue = False
        print("------Empty Fitting Room------")
    else:
        ctr = 1


def green_enter():
    global fitting_room, green_access
    global greenCtr, blueCtr, b, g, quantum

    # wait for blue threads to release the lock for the fitting room
    while blue_access.locked():
        pass

    # acquire the access to the fitting room for the green threads
    if not green_access.locked():
        green_access.acquire()
        print("----------Green Only----------")

    with fitting_room:
        print(threading.current_thread().name)
        greenCtr += 1
        time.sleep(1)

    # if all green threads are finished or the number of green threads
    # reached the quantum that was set, pass the access to blue threads
    if greenCtr == g or greenCtr % quantum == 0:
        print("------Empty Fitting Room------")
        green_access.release()

    while blue_access.locked() == False and blueCtr != b:
        pass


def blue_enter():
    global fitting_room, green_access, blue_access
    global greenCtr, blueCtr, b, g, quantum

    # wait for green threads to release the lock for the fitting room
    while green_access.locked():
        pass

    # acquire the access to the fitting room for the blue threads
    if not blue_access.locked():
        blue_access.acquire()
        print("----------Blue Only-----------")

    with fitting_room:
        print(threading.current_thread().name)
        blueCtr += 1
        time.sleep(1)

    # if all blue threads are finished or the number of blue threads
    # reached the quantum that was set, pass the access to green threads
    if blueCtr == b or blueCtr % quantum == 0:
        print("------Empty Fitting Room------")
        blue_access.release()

    while green_access.locked() == False and greenCtr != g:
        pass


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

for thread in threads:
    thread.join()
