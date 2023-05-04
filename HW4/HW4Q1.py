import SimFunctions
import SimRNG
import SimClasses
import numpy as np
import scipy.stats as stats

ZSimRNG = SimRNG.InitializeRNSeed()
Calendar = SimClasses.EventCalendar()


def t_mean_confidence_interval(data, alpha):  # compute the CI with set alpha
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = stats.t.ppf(1 - alpha / 2, n - 1) * se
    return m, m - h, m + h


SimClasses.Clock = 0

Inventory = SimClasses.CTStat()
Totalcost = 0

TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

I = 60  # update the inventory
t = 0  # update the event time whenever there is a change in inventory
a = 0  # update the amount of orders
TheCTStats.append(Inventory)
AllTotalcost = []


# Demand function
def demandschedule(D):
    if SimRNG.Uniform(0, 1, 2) <= 1 / 6:
        return D[0]
    elif SimRNG.Uniform(0, 1, 2) <= 1 / 2:
        return D[1]
    elif SimRNG.Uniform(0, 1, 2) <= 5 / 6:
        return D[2]
    else:
        return D[3]


D = [1, 2, 3, 4]
meandt = 0.1
meanrt = 0.75

# Cost of ordering
K = 32  # fixed cost
i = 3  # variable cost per item

# cost of inventory
h = 1  # per item per month
pi = 5  # backlog cost

T = 120  # run length
# reorder point and order to point
s = 30
S = 100

repN = 500  # number of replications
Stream = 2 # use the same stream for all random numbers


def update_hcost(inventory, time):
    global Totalcost
    if inventory >= 0:
        Totalcost += inventory * h * (SimClasses.Clock - time)  # holding cost
    else:
        Totalcost += abs(inventory) * pi * (SimClasses.Clock - time)  # backlog cost


def Shipping():  # ship out or use inventory to satisfy demand
    global Totalcost
    global I
    global t
    update_hcost(I, t)
    I -= demandschedule(D)
    Inventory.Record(max(0, I))
    t = SimClasses.Clock
    SimFunctions.Schedule(Calendar, "Shipping", SimRNG.Expon(meandt, Stream))
    # meet demand use inventory
    # update inventory level and compute cost


def Ordering():  # check invenotry level and make orders
    global Totalcost
    global I
    global t
    global a
    if I < s and a == 0:  # make orders and update totalcost by ordering cost
        a = S - I
        # Schedule receiving
        SimFunctions.Schedule(Calendar, "Receiving", SimRNG.Erlang(2, meanrt, Stream))
        Totalcost += K + a * i
    SimFunctions.Schedule(Calendar, "Ordering", 1)


def Receiving():
    global Totalcost
    global I
    global t
    global a
    update_hcost(I, t)
    I += a  # update inventory level
    Inventory.Record(max(0, I))
    t = SimClasses.Clock
    a = 0  # reset order amount


for reps in range(0, repN, 1):
    Totalcost = 0  # Reset the cost for  each replication
    I = 60
    t = 0
    a = 0
    SimFunctions.SimFunctionsInit(Calendar, TheQueues, TheCTStats, TheDTStats, TheResources)
    SimFunctions.Schedule(Calendar, "Shipping", SimRNG.Expon(meandt, Stream))
    SimFunctions.Schedule(Calendar, "Ordering", 1)
    SimFunctions.Schedule(Calendar, "EndSimulation", T)

    NextEvent = Calendar.Remove()
    SimClasses.Clock = NextEvent.EventTime
    if NextEvent.EventType == "Shipping":
        Shipping()
    elif NextEvent.EventType == "Ordering":
        Ordering()
    elif NextEvent.EventType == "Receiving":
        Receiving()

    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        SimClasses.Clock = NextEvent.EventTime
        if NextEvent.EventType == "Shipping":
            Shipping()
        elif NextEvent.EventType == "Ordering":
            Ordering()
        elif NextEvent.EventType == "Receiving":
            Receiving()

    AllTotalcost.append(Totalcost)
    # print(Inventory.Mean())
#print("Estimate average cost with a 95% CI is: ", t_mean_confidence_interval(AllTotalcost, 0.05))
print("Estimate average cost is: ", np.mean(AllTotalcost))
print("Estimate variance of total cost is: ", np.var(AllTotalcost))