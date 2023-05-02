import SimClasses
import SimFunctions
import SimRNG
import math
import pandas
import numpy as np

ZSimRNG = SimRNG.InitializeRNSeed()

Queue = SimClasses.FIFOQueue()
Wait = SimClasses.DTStat()
Lost = SimClasses.DTStat()
Server = SimClasses.Resource()
Calendar = SimClasses.EventCalendar()

TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

TheDTStats.append(Wait)
TheDTStats.append(Lost)
TheQueues.append(Queue)
TheResources.append(Server)


Server.SetUnits (1)
MeanTBA = 10
# ST = Unifrom (5,12)
Phases = 3
RunLength = 500000 # unit in min

QueueLength = [] # QueueLength records the number of queue

AllWaitMean = []
AllQueueMean = []
AllQueueNum = []
AllServerMean = []
AllLostMean = []
Capacity = [] # 95% of quantile of sorted QueueLength

print ("Rep", "Average Wait", "Server Utilization", "95% Quantile of Queue", "Total # of Callers", "Callers Loss")


def Callin():
    global QueueLength
    SimFunctions.Schedule(Calendar, "Callin", SimRNG.Expon(MeanTBA, 1))
    Caller = SimClasses.Entity()
    Queue.Add(Caller)

    if Server.Busy == 0:
        Server.Seize(1)
        NextCaller = Queue.Remove()
        Wait.Record(SimClasses.Clock - NextCaller.CreateTime)
        SimFunctions.SchedulePlus(Calendar, "EndCall", SimRNG.Uniform(5, 12, 1),NextCaller)
        Lost.Record(0) # Lost count 0, caller not lost
    elif SimRNG.Uniform(0, 1, 1) < 0.1: # 10% chance the caller hangup if not served immediately
        Queue.Remove()
        Lost.Record(0) # Lost count 0, caller not lost
    elif Queue.NumQueue() > 5: # Choose the capacity of 5
        Queue.Remove()
        Lost.Record(1) # Lost count 1, caller lost
    QueueLength.append(Queue.NumQueue()) # Record the Queue length after each Callin

def EndCall():
    Server.Free(1)
    if Queue.NumQueue() > 0:
        Server.Seize(1)
        NextCaller = Queue.Remove()
        Wait.Record(SimClasses.Clock - NextCaller.CreateTime)
        SimFunctions.SchedulePlus(Calendar, "EndCall", SimRNG.Uniform(5, 12, 1),NextCaller)


for reps in range(0, 10, 1):

    SimFunctions.SimFunctionsInit(Calendar, TheQueues, TheCTStats, TheDTStats, TheResources)
    SimFunctions.Schedule(Calendar, "Callin", SimRNG.Expon(MeanTBA, 1))
    SimFunctions.Schedule(Calendar, "EndSimulation", RunLength)

    QueueLength = []

    NextEvent = Calendar.Remove()
    SimClasses.Clock = NextEvent.EventTime
    if NextEvent.EventType == "Callin":
        Callin()
    elif NextEvent.EventType == "EndCall":
        EndCall()

    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        SimClasses.Clock = NextEvent.EventTime
        if NextEvent.EventType == "Callin":
            Callin()
        elif NextEvent.EventType == "EndCall":
            EndCall()

    AllWaitMean.append(Wait.Mean())
    AllServerMean.append(Server.Mean())
    AllLostMean.append(Lost.Mean())
    Quantile95 = int(np.ceil(0.95*len(QueueLength)))
    Capacity.append(np.sort(QueueLength)[Quantile95])
    print(reps + 1,"  ", Wait.Mean(), "  ",Server.Mean(), "  ",Capacity[-1],"  ",len(QueueLength), Lost.Mean())

# output results
print("Estimated required queue capacity for less than 5% loss of callers is:",np.mean(Capacity))
print("Estimated Expected Average loss of callers:", np.mean(AllLostMean))
print("Estimated Expected Average wait:", np.mean(AllWaitMean))
print("Estimated Expected Average utilization:", np.mean(AllServerMean))