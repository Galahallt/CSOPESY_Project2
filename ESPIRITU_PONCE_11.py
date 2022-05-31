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

    global isBlue
    isBlue = True

    if (g < b):
        # print("----------Green Only----------")
        isBlue = False
    # else:
        # print("----------Blue Only----------")

    ctr = 0
    blueCtr = 0
    greenCtr = 0
    quantum = 2

    for i in range(b + g):
        if isBlue and blueCtr < b:
            if ctr == 0:
                print("----------Blue Only----------")

            # create blue thread
            blue = threading.Thread(
                target=blue_enter, name="Thread ID: " + str(threadId) + " | Color: Blue"
            )
            # start blue thread
            blue.start()
            time.sleep(1)

            blueCtr+=1
        else:
            if ctr == 0:
                print("----------Green Only----------")

            # create green thread
            green = threading.Thread(
                target=green_enter, name="Thread ID: " + str(threadId) + " | Color: Green"
            )
            # start green thread
            green.start()
            time.sleep(1)

            greenCtr+=1
        
        # if quantum reached, switch to other color
        if ctr == quantum:
            # if alternating
            if blueCtr < b and greenCtr < g:
                ctr = 0
                isBlue = not isBlue
                print("------Empty Fitting Room------")

            # if non-alternating
            else:
                if blueCtr < b:
                    isBlue = True
                else:
                    isBlue = False

        # else, just increment counter
        else:
            ctr+=1
    
    print("------Empty Fitting Room------")
    # print(fitting_room.__dict__)
        

    # print("----------Blue Only----------")
    # for i in range(b):
    #     # create blue thread
    #     blue = threading.Thread(
    #         target=blue_enter, name="Thread ID: " + str(threadId) + " | Color: Blue"
    #     )
    #     # start blue thread
    #     blue.start()
    #     time.sleep(1)
    # print("------Empty Fitting Room------")

    # print("----------Green Only----------")
    # for j in range(g):
    #     # create green thread
    #     green = threading.Thread(
    #         target=green_enter, name="Thread ID: " + str(threadId) + " | Color: Green"
    #     )
    #     # start green thread
    #     green.start()
    #     time.sleep(1)
    # print("------Empty Fitting Room------")
