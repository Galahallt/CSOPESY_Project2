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
import logging


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
    # # if non-alternating
    # else:
    #     # there are still blue threads to be executed
    #     if blueCtr < b:
    #         isBlue = True
    #     # there are still green threads to be executed
    #     else:
    #         isBlue = False


# def green_enter():
#     global fitting_room, greenCtr
#     fitting_room.acquire()

#     print(threading.current_thread().name)

#     # threadId += 1
#     greenCtr += 1

#     change_thread()
#     time.sleep(1)

#     fitting_room.release()


# def blue_enter():
#     global fitting_room, blueCtr
#     fitting_room.acquire()

#     print(threading.current_thread().name)

#     # threadId += 1
#     blueCtr += 1

#     change_thread()
#     time.sleep(1)

#     fitting_room.release()

# def thread_function():
    # logging.info("Tread Starting: " + threading.current_thread().name)
    # time.sleep(2) # do work
    # logging.info("Tread Finishing: " + threading.current_thread().name)
    
def blue_enter():
    global fitting_room, blue_threads, blue_lock, green_lock
    global blue_exec_ctr, n, b, slot

    # if no locks claimed, claim blue lock
    if not(blue_lock.locked()) and not(green_lock.locked()):
        blue_lock.acquire()
        print("Blue Only")

    # while green lock is claimed, do nothing
    while green_lock.locked():
        pass

    # enter fitting room
    fitting_room.acquire()
    print(threading.current_thread().name)
    time.sleep(1)   # do something

    # leave fitting room
    fitting_room.release()
    blue_threads.pop()
    blue_exec_ctr += 1
    slot += 1

    # if last in fitting room, give room to green
    if slot == n or blue_exec_ctr == b:
        blue_lock.release()
        green_lock.acquire()
        slot = 0
        print("Empty Fitting Room")
        print("Green Only")
    
def green_enter():
    global fitting_room, blue_threads, blue_lock, green_lock
    global green_exec_ctr, n, g, slot
    
    if not(blue_lock.locked()) and not(green_lock.locked()):
        green_lock.acquire()
        print("Green Only")

    while blue_lock.locked():
        pass

    fitting_room.acquire()
    print(threading.current_thread().name)
    time.sleep(1)
    fitting_room.release()
    green_threads.pop()

    green_exec_ctr += 1
    slot += 1

    if slot == n or green_exec_ctr == g:
        green_lock.release()
        blue_lock.acquire()
        slot = 0
        print("Empty Fitting Room")
        print("Blue Only")


if __name__ == "__main__":
    # for logging
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    global n, b, g
    n, b, g = list(
        map(int, input("Enter 3 space-separated integers (n, b, g): ").split())
    )

    # initialize n slots inside fitting room
    global fitting_room
    fitting_room = threading.BoundedSemaphore(value=n)

    # blue-green restriction lock
    global blue_lock, green_lock
    blue_lock = threading.Lock()
    green_lock = threading.Lock()

    global blue_exec_ctr, green_exec_ctr, slot
    blue_exec_ctr = green_exec_ctr = slot = n

    # list of threads
    global blue_threads, green_threads
    blue_threads = list()
    green_threads = list()

    # create & run threads
    for i in range (b + g):
        x = None
        if (i < b):
            x = threading.Thread(target=blue_enter, name="Thread ID: " + str(i) + " | Color: Blue")
            blue_threads.append(x)
        else:
            x = threading.Thread(target=green_enter, name="Thread ID: " + str(i) + " | Color: Green")
            green_threads.append(x)
        
        x.start()
    
    # print(len(thread_list))