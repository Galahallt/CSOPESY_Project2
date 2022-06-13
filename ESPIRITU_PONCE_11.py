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

def blue_enter():
    global fitting_room, blue_semaphore, green_semaphore, blue_room_mutex, green_room_mutex
    global blue_exec_ctr, green_exec_ctr, b, g, quantum

    # request for blue access into the room
    blue_semaphore.acquire()

    # wait for green mutex lock to be released
    while green_room_mutex.locked():
        pass

    # if blue mutex lock is not yet acquired, acquire it.
    if not blue_room_mutex.locked():
        # acquire blue mutex lock
        blue_room_mutex.acquire()
        # indicate that the fitting room is for blue threads only
        print("Blue only.")

    # request for access into the room
    fitting_room.acquire()

    # display thread details
    print(threading.current_thread().name)

    # do something
    time.sleep(1)

    # acquire blue counter mutex lock
    blue_ctr_mutex.acquire()
    # +1 blue thread executed
    blue_exec_ctr += 1

    # if first blue process and there are green threads waiting,
    if blue_exec_ctr % quantum == 1 and green_exec_ctr <= g:

        # if all green threads has been executed already,
        if green_exec_ctr == g and g > 0:
            # then +1 for green_exec_ctr to avoid printing "Blue Only."
            # when blue threads are no longer giving the room to
            # green threads
            green_ctr_mutex.acquire()
            green_exec_ctr += 1
            green_ctr_mutex.release()

    # if all blue threads are done executing already OR
    # quantum has been reached AND there are still green threads waiting
    if (blue_exec_ctr % quantum == 0 and green_exec_ctr <= g) or blue_exec_ctr == b:

        # if there are green threads waiting,
        if green_exec_ctr < g:
            # release semaphores for green threads
            for i in range(quantum):
                green_semaphore.release()

            # release blue mutex lock
            blue_room_mutex.release()

        # signal that the room is empty
        print("Empty fitting room.")

    # release blue counter mutex lock
    blue_ctr_mutex.release()

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

    # wait for blue mutex lock to be reelased
    while blue_room_mutex.locked():
        pass

    # if green mutex lock is not yet acquired, acquire it.
    if not green_room_mutex.locked():
        # acquire green mutex lock
        green_room_mutex.acquire()
        # indicate that the fitting room is for green threads only
        print("Green only.")

    # request for access into the room
    fitting_room.acquire()

    # display thread details
    print(threading.current_thread().name)

    # do something
    time.sleep(1)

    # acquire green counter mutex lock
    green_ctr_mutex.acquire()
    # +1 green thread executed
    green_exec_ctr += 1

    # if first green process and there are blue threads waiting,
    if green_exec_ctr % quantum == 1 and blue_exec_ctr <= b:

        # if all blue threads has been executed already,
        if blue_exec_ctr == b and b > 0:
            # then +1 for blue_exec_ctr to avoid printing "Green Only."
            # when green threads are no longer giving the room to
            # blue threads
            blue_ctr_mutex.acquire()
            blue_exec_ctr += 1
            blue_ctr_mutex.release()

    # if all green threads are done executing already OR
    # quantum has been reached AND there are still blue threads waiting
    if (green_exec_ctr % quantum == 0 and blue_exec_ctr <= b) or green_exec_ctr == g:

        # if there are blue threads waiting,
        if blue_exec_ctr < b:
            # release semaphores for blue threads
            for i in range(quantum):
                blue_semaphore.release()

            # release green mutex lock
            green_room_mutex.release()

        # signal that the room is empty
        print("Empty fitting room.")

    # release green counter mutex lock
    green_ctr_mutex.release()

    # release the acquired fitting room lock / semaphore value
    fitting_room.release()

    # if no blue thread is waiting anymore,
    if blue_exec_ctr >= b:
        # then just release locks for other green threads
        green_semaphore.release()

# ask for input
n, b, g = list(map(int, input("Enter 3 space-separated integers (n, b, g): ").split()))

# initialize n slots inside fitting room
fitting_room = threading.BoundedSemaphore(value=n)

# limit value per "turn"
quantum = n

# if there are no green threads,
if b > 0 and g == 0:
    # just execute the blue threads
    blue_semaphore = threading.Semaphore(value=quantum)
    green_semaphore = threading.Semaphore(value=0)
# if there are no blue threads, 
elif g > 0 and b == 0:
    # just execute the green threads
    blue_semaphore = threading.Semaphore(value=0)
    green_semaphore = threading.Semaphore(value=quantum)
# if there are more green threads than blue threads,
elif b < g:
    # then blue threads goes first
    blue_semaphore = threading.Semaphore(value=quantum)
    green_semaphore = threading.Semaphore(value=0)
# if there are more blue threads than green threads,
elif g < b:
    # then green threads goes first
    blue_semaphore = threading.Semaphore(value=0)
    green_semaphore = threading.Semaphore(value=quantum)
# else,
else:
    print("Invalid Input! There must be at least one green or blue thread!")

# set counters for no. of blue and green threads that finished executing
green_exec_ctr = blue_exec_ctr = 0

# thread counter mutex locks
blue_ctr_mutex = threading.Lock()
green_ctr_mutex = threading.Lock()

# fitting room color access mutex lock
blue_room_mutex = threading.Lock()
green_room_mutex = threading.Lock()

# list of threads created
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

# wait until the blue and green threads terminate
# for thread in threads:
#     thread.join()
