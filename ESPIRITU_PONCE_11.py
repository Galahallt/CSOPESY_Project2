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

    # request for blue access into the room
    blue_access.acquire()
    # request for access into the room
    fitting_room.acquire()
    
    # +1 blue thread executed
    blue_ctr_access.acquire()
    blueCtr += 1
    blue_ctr_access.release()

    # if first blue process and there are green threads waiting,
    if blueCtr % quantum == 1 and greenCtr <= g:
        # indicate that the waiting room is for blue threads only
        print("Blue Only.")

        # if all green threads has been executed already,
        if greenCtr == g:
            # then +1 for greenCtr to avoid printing "Blue Only."
            # when blue threads are no longer giving the room to
            # green threads
            green_ctr_access.acquire()
            greenCtr += 1
            green_ctr_access.release()

    # if blueCtr % quantum == 0 or blueCtr >= b:
    #     print("Empty fitting room.")

    # display thread details
    print(threading.current_thread().name)
    
    # do something
    time.sleep(0.5)

    # release the acquired fitting room lock / semaphore value
    fitting_room.release()

    # if there are green threads waiting to enter the fitting room.
    if greenCtr < g:
        # create a lock that can be acquired by a green thread
        green_access.release()
    # else, just release the lock for this blue slot
    else:
        blue_access.release()



def green_enter():
    global fitting_room, blue_access, green_access
    global blueCtr, greenCtr, b, g, quantum

    # request for green access into the room
    green_access.acquire()
    # request for access into the room
    fitting_room.acquire()

    # +1 green thread executed
    green_ctr_access.acquire()
    greenCtr += 1
    green_ctr_access.release()

    # if first green process and there are blue threads waiting,
    if greenCtr % quantum == 1 and blueCtr <= b:
        # indicate that the waiting room is for green threads only
        print("Green Only.")

        # if all blue threads has been executed already,
        if blueCtr == b:
            # then +1 for blueCtr to avoid printing "Green Only."
            # when green threads are no longer giving the room to
            # blue threads
            blue_ctr_access.acquire()
            blueCtr += 1
            blue_ctr_access.release()

    # if greenCtr % quantum == 0 or greenCtr >= g:
    #     print("Empty fitting room.")
    
    # display thread details
    print(threading.current_thread().name)
    
    # do something
    time.sleep(0.5)

    # release the acquired fitting room lock / semaphore value
    fitting_room.release()

    # if there are blue threads waiting to enter the fitting room.
    if blueCtr < b:
        # create a lock that can be acquired by a blue thread
        blue_access.release()
    # else, just release the lock for this green slot
    else:
        green_access.release()



n, b, g = list(map(int, input("Enter 3 space-separated integers (n, b, g): ").split()))

# initialize n slots inside fitting room
fitting_room = threading.BoundedSemaphore(value=n)

# green_access = threading.Lock()
# blue_access = threading.Lock()

quantum = n

# use semaphores instead of mutex locks
# for now, blue goes first
blue_access = threading.Semaphore(value=quantum)
green_access = threading.Semaphore(value=0)

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
