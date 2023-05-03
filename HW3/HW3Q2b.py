import SimClasses
import SimFunctions
import SimRNG
import math
import numpy as np
import scipy.stats as stats

SimClasses.Clock = 0
MeanAR = [60,240,120] # The call arrival rate in hourly
QueueLength = SimClasses.CTStat() # record the number of drones busy
N = 0
MaxQueue = 0
RepNum = 1000
MeanBusy = 0.75 # The mean time for drones to be busy after call

ZSimRNG = SimRNG.InitializeRNSeed()
Calendar = SimClasses.EventCalendar()

TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

TheCTStats.append(QueueLength)

AllQueueLength = []
AllMaxQueue = []
AllN = []

def t_mean_confidence_interval(data,alpha): # compute the CI with set alpha
    a = 1.0 * np.array(data)
    n = len (a)
    m, se = np.mean(a), stats.sem(a)
    h = stats.t.ppf(1 - alpha /2,n-1)*se
    return m, m-h, m+h

def NSPP(MeanAR, Stream):
    ar = 240
    PossibleArrival = SimClasses.Clock + SimRNG.Expon(1/max(MeanAR), Stream)
    if SimClasses.Clock <= 7:
        ar = MeanAR[0]
    elif 7 < SimClasses.Clock <= 17:
        ar = MeanAR[1]
    elif 17 < SimClasses.Clock <= 24:
        ar = MeanAR[2]

    if SimRNG.Uniform(0, 1, Stream) <= ar/ max(MeanAR):
        PossibleArrival = PossibleArrival + SimRNG.Expon(1/max(MeanAR), Stream)
    nspp = PossibleArrival - SimClasses.Clock
    return nspp

def Callin():
    global MaxQueue
    global N
    interarrival = NSPP(MeanAR,1)
    SimFunctions.Schedule(Calendar, "Callin", interarrival)
    N = N + 1
    QueueLength.Record(N)
    if N > MaxQueue:
        MaxQueue = N
    SimFunctions.Schedule(Calendar, "ReadyDrone", SimRNG.Expon(MeanBusy, 2))


def ReadyDrone():
    global N
    N = N - 1
    QueueLength.Record(N)


for Reps in range(0, RepNum, 1):
    N = 0
    MaxQueue = 0
    SimFunctions.SimFunctionsInit(Calendar, TheQueues, TheCTStats, TheDTStats, TheResources)
    interarrival = NSPP(MeanAR,1)
    SimFunctions.Schedule(Calendar, "Callin", interarrival)
    SimFunctions.Schedule(Calendar, "EndSimulation", 24)

    NextEvent = Calendar.Remove()
    SimClasses.Clock = NextEvent.EventTime
    if NextEvent.EventType == "Callin":
        Callin()
    elif NextEvent.EventType == "ReadyDrone":
        ReadyDrone()

    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        SimClasses.Clock = NextEvent.EventTime
        if NextEvent.EventType == "Callin":
            Callin()
        elif NextEvent.EventType == "ReadyDrone":
            ReadyDrone()

    AllQueueLength.append(QueueLength.Mean())
    AllMaxQueue.append(MaxQueue)
    AllN.append(N)

    #print(Reps+1, QueueLength.Mean(), MaxQueue, N)
# estimating the 0.98th quantile
quantile_index = int(np.ceil(RepNum * 0.98) - 1)
capacity = np.sort(AllMaxQueue)[quantile_index]
capacitylb95 = np.floor(capacity - 1.96 * np.sqrt(capacity *(1-0.98)))
capacityub95 = np.ceil(capacity + 1.96 * np.sqrt(capacity *(1-0.98)))
print("Estimated required minimum number of drones is:", capacity, capacitylb95, capacityub95)
print("Estimated Expected Average # of drones busy is:", t_mean_confidence_interval(AllQueueLength,0.05))
print("Estimated Expected Max # of drones busy:", t_mean_confidence_interval(AllMaxQueue,0.05))