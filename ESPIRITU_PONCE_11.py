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

    # print(threading.current_thread().name)

def blue_enter():
    global fitting_room, blue_access, green_access
    global blueCtr, greenCtr, b, g, quantum

    blue_access.acquire()
    fitting_room.acquire()
    
    blue_ctr_access.acquire()
    blueCtr += 1
    blue_ctr_access.release()

    if blueCtr % quantum == 1 and greenCtr <= g:
        # print("Empty fitting room.")
        print("Blue Only.")

        if greenCtr == g:
            green_ctr_access.acquire()
            greenCtr += 1
            green_ctr_access.release()

    print(threading.current_thread().name)

    time.sleep(0.5)
    fitting_room.release()

    if greenCtr < g:
        green_access.release()
    else:
        blue_access.release()


def green_enter():
    global fitting_room, blue_access, green_access
    global blueCtr, greenCtr, b, g, quantum

    green_access.acquire()
    fitting_room.acquire()

    green_ctr_access.acquire()
    greenCtr += 1
    green_ctr_access.release()

    if greenCtr % quantum == 1 and blueCtr <= b:
        # print("Empty fitting room.")
        print("Green Only.")

        if blueCtr == b:
            blue_ctr_access.acquire()
            blueCtr += 1
            blue_ctr_access.release()
    
    print(threading.current_thread().name)
    
    time.sleep(0.5)
    fitting_room.release()

    if blueCtr < b:
        blue_access.release()
    else:
        green_access.release()


n, b, g = list(map(int, input("Enter 3 space-separated integers (n, b, g): ").split()))

# initialize n slots inside fitting room
fitting_room = threading.BoundedSemaphore(value=n)

print(fitting_room.__dict__)

# green_access = threading.Lock()
# blue_access = threading.Lock()

quantum = n

blue_access = threading.Semaphore(value=quantum)
green_access = threading.Semaphore(value=0)

print(blue_access.__dict__)

greenCtr = blueCtr = 0

blue_ctr_access = threading.Lock()
green_ctr_access = threading.Lock()

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
