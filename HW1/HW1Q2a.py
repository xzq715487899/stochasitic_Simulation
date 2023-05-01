import numpy as np
import matplotlib.pyplot as plt

# start with 2 functioning components at time 0
clock = 0
S = 2

# fix random number seed
np.random.seed(1)

# initialize the time of events
NextRepair = float('inf')
NextFailure = np.ceil(6 * np.random.random())
# lists to keep the event times and the states
EventTimes = [0]
States = [2]

while clock < 10:
    # advance the time
    clock = min(NextRepair, NextFailure)

    if NextRepair < NextFailure:
        # next event is completion of a repair
        S = S + 1
        NextRepair = float('inf')
    else:
        # next event is a failure
        S = S - 1
        if S == 1:
            NextRepair = clock + 2.5
            NextFailure = clock + np.ceil(6 * np.random.random())

    # save the time and state
    EventTimes.append(clock)
    States.append(S)

EventTimes
States