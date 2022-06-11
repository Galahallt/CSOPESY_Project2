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

from math import *

    # print(threading.current_thread().name)

def blue_enter():
    global fitting_room, blue_semaphore, green_semaphore, blue_room_mutex, green_room_mutex
    global blue_exec_ctr, green_exec_ctr, b, g, quantum

    # request for blue access into the room
    blue_semaphore.acquire()

    # blue_room_mutex
    while green_room_mutex.locked():
        pass
    
    if not blue_room_mutex.locked():
        blue_room_mutex.acquire()

    # request for access into the room
    fitting_room.acquire()
    
    # +1 blue thread executed
    blue_ctr_mutex.acquire()
    blue_exec_ctr += 1

    # if first blue process and there are green threads waiting,
    if blue_exec_ctr % quantum == 1 and green_exec_ctr <= g:
        # indicate that the waiting room is for blue threads only
        print("Blue Only.")

        # if all green threads has been executed already,
        if green_exec_ctr == g:
            # then +1 for green_exec_ctr to avoid printing "Blue Only."
            # when blue threads are no longer giving the room to
            # green threads
            green_ctr_mutex.acquire()
            green_exec_ctr += 1
            green_ctr_mutex.release()

    # display thread details
    print(threading.current_thread().name)

    # if done already (quantum is met OR no blue threads left) AND
    # there are green threads waiting OR this is the last blue thread
    if (blue_exec_ctr % quantum == 0 or blue_exec_ctr == b) and (green_exec_ctr <= g or blue_exec_ctr == b):

        # if there are green threads waiting,
        if green_exec_ctr < g:
            # release locks for green threads
            for i in range(quantum):
                green_semaphore.release()

        blue_room_mutex.release()
        print("Empty room.")

    # release blue_ctr_mutex lock
    blue_ctr_mutex.release()

    # do something
    time.sleep(1)

    # release the acquired fitting room lock / semaphore value
    fitting_room.release()
    
    # if no green thread is waiting anymore,
    if green_exec_ctr >= g:
        # then just release locks for other blue threads
        blue_semaphore.release()


def green_enter():
    global fitting_room, blue_semaphore, green_semaphore, blue_room_mutex, green_room_mutex
    global blue_exec_ctr, green_exec_ctr, b, g, quantum

    # request for green access into the room
    green_semaphore.acquire()

    # 
    while blue_room_mutex.locked():
        pass
    
    if not green_room_mutex.locked():
        green_room_mutex.acquire()

    # request for access into the room
    fitting_room.acquire()

    # +1 green thread executed
    green_ctr_mutex.acquire()
    green_exec_ctr += 1

    # if first green process and there are blue threads waiting,
    if green_exec_ctr % quantum == 1 and blue_exec_ctr <= b:
        # indicate that the waiting room is for green threads only
        print("Green Only.")

        # if all blue threads has been executed already,
        if blue_exec_ctr == b:
            # then +1 for blue_exec_ctr to avoid printing "Green Only."
            # when green threads are no longer giving the room to
            # blue threads
            blue_ctr_mutex.acquire()
            blue_exec_ctr += 1
            blue_ctr_mutex.release()

    # display thread details
    print(threading.current_thread().name)

    # if done already (quantum is met OR no green threads left) AND
    # there are blue threads waiting OR this is the last green thread
    if (green_exec_ctr % quantum == 0 or green_exec_ctr == g) and (blue_exec_ctr <= b or green_exec_ctr == g):
        
        # if there are blue threads waiting,
        if blue_exec_ctr < b:
            # release locks for blue threads
            for i in range(quantum):
                blue_semaphore.release()

        green_room_mutex.release()
        print("Empty room.")

    # release green_ctr_mutex lock
    green_ctr_mutex.release()
    
    # do something
    time.sleep(1)

    # release the acquired fitting room lock / semaphore value
    fitting_room.release()
    
    # if no blue thread is waiting anymore,
    if blue_exec_ctr >= b:
        # then just release locks for other green threads
        green_semaphore.release()


"""
(1) 3 7 11, 3 2 4 test case
(2) Random printing
"""

n, b, g = list(map(int, input("Enter 3 space-separated integers (n, b, g): ").split()))

# initialize n slots inside fitting room
fitting_room = threading.BoundedSemaphore(value=n)

# green_semaphore = threading.Lock()
# blue_semaphore = threading.Lock()

quantum = n

# use semaphores instead of mutex locks
# for now, blue goes first
if b < g:
    blue_semaphore = threading.Semaphore(value=quantum)
    green_semaphore = threading.Semaphore(value=0)
else:
    blue_semaphore = threading.Semaphore(value=0)
    green_semaphore = threading.Semaphore(value=quantum)

green_exec_ctr = blue_exec_ctr = 0

blue_ctr_mutex = threading.Lock()
green_ctr_mutex = threading.Lock()

blue_room_mutex = threading.Lock()
green_room_mutex = threading.Lock()

# run until the number of blue and green threads are reached
for i in range(b + g):
    if i < b:
        blue = threading.Thread(
            target=blue_enter, name="Thread ID: " + str(i) + " | Color: Blue"
        )
        blue.start()
    else:
        green = threading.Thread(
            target=green_enter, name="Thread ID: " + str(i) + " | Color: Green"
        )
        green.start()