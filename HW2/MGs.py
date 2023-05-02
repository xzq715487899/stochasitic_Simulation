import SimFunctions
import SimRNG
import SimClasses
import numpy as np
import pandas

ZSimRNG = SimRNG.InitializeRNSeed()

Queue = SimClasses.FIFOQueue()
Wait = SimClasses.DTStat()
Server = SimClasses.Resource()
Calendar = SimClasses.EventCalendar()

TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

TheDTStats.append(Wait)
TheQueues.append(Queue)
TheResources.append(Server)

s = 30 # the number of servers s = 20 s = 30
Server.SetUnits(s)
MeanTBA = 1/s # lamda = s, so arrival interval is 1/s
MeanST = 0.8
Phases = 3
RunLength = 5500
WarmUp = 500

AllWaitMean = []
AllQueueMean = []
AllQueueNum = []
AllServerMean = []
print("Rep", "Average Wait", "Average Number in Queue", "Number Remaining in Queue", "Server Utilization")


def Arrival():
    SimFunctions.Schedule(Calendar, "Arrival", SimRNG.Expon(MeanTBA, 1))
    Customer = SimClasses.Entity()
    Queue.Add(Customer)

    if Server.Busy < s:
        Server.Seize(1)
        NextCustomer = Queue.Remove() # customer leaves the queue if served
        SimFunctions.SchedulePlus(Calendar, "EndOfService", SimRNG.Erlang(Phases, MeanST, 2), NextCustomer)


def EndOfService(DepartingCustomer): # give an object to the EndOfService function to record total time in system
    Wait.Record(SimClasses.Clock - DepartingCustomer.CreateTime) # Record the customer's total time in system
    Server.Free(1)

    if Queue.NumQueue() > 0:
        Server.Seize(1)
        NextCustomer = Queue.Remove()
        SimFunctions.SchedulePlus(Calendar, "EndOfService", SimRNG.Erlang(Phases, MeanST, 2), NextCustomer)

for reps in range(0, 10, 1):

    SimFunctions.SimFunctionsInit(Calendar, TheQueues, TheCTStats, TheDTStats, TheResources)
    SimFunctions.Schedule(Calendar, "Arrival", SimRNG.Expon(MeanTBA, 1))
    SimFunctions.Schedule(Calendar, "EndSimulation", RunLength)
    SimFunctions.Schedule(Calendar, "ClearIt", WarmUp)

    NextEvent = Calendar.Remove()
    SimClasses.Clock = NextEvent.EventTime
    if NextEvent.EventType == "Arrival":
        Arrival()
    elif NextEvent.EventType == "EndOfService":
        EndOfService(NextEvent.WhichObject)
    elif NextEvent.EventType == "ClearIt":
        SimFunctions.ClearStats(TheCTStats, TheDTStats)

    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        SimClasses.Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "EndOfService":
            EndOfService(NextEvent.WhichObject)
        elif NextEvent.EventType == "ClearIt":
            SimFunctions.ClearStats(TheCTStats, TheDTStats)

    AllWaitMean.append(Wait.Mean())
    AllQueueMean.append(Queue.Mean())
    AllQueueNum.append(Queue.NumQueue())
    AllServerMean.append(Server.Mean() / s) # compute the utilization of servers
    print(reps + 1, Wait.Mean(), Queue.Mean(), Queue.NumQueue(), Server.Mean() / s)

# output results

print("Estimated Expected System Time:", np.mean(AllWaitMean))
print("Estimated Expected Average queue-length:", np.mean(AllQueueMean))
print("Estimated Expected Average utilization:", np.mean(AllServerMean))

