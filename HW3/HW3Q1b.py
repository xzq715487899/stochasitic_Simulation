import SimFunctions
import SimRNG
import SimClasses
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def t_mean_confidence_interval(data,alpha): # compute the CI with set alpha
    a = 1.0 * np.array(data)
    n = len (a)
    m, se = np.mean(a), stats.sem(a)
    h = stats.t.ppf(1 - alpha /2,n-1)*se
    return m, m-h, m+h

ZSimRNG = SimRNG.InitializeRNSeed()

# set the queues and servers
Queue_clean = SimClasses.FIFOQueue()
Queue_load = SimClasses.FIFOQueue()
Queue_oxidize = SimClasses.FIFOQueue()
Queue_unload = SimClasses.FIFOQueue()
Server_clean = SimClasses.Resource()
Server_load = SimClasses.Resource()
Server_oxidize = SimClasses.Resource()
Server_unload = SimClasses.Resource()
TotalTime1 = SimClasses.DTStat()
TotalTime2 = SimClasses.DTStat()
Calendar = SimClasses.EventCalendar()


TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

TheDTStats.append(TotalTime1)
TheDTStats.append(TotalTime2)
TheQueues.append(Queue_clean)
TheQueues.append(Queue_load)
TheQueues.append(Queue_oxidize)
TheQueues.append(Queue_unload)
TheResources.append(Server_clean)
TheResources.append(Server_load)
TheResources.append(Server_oxidize)
TheResources.append(Server_unload)

# standard setup but only Totaltime are used
AllQueue_clean = []
AllQueue_load = []
AllQueue_oxidize = []
AllQueue_unload = []
AllTotalTime1 = []
AllMeanTC = []
AllMeanTD = []
AllTotalTime2 = []
AllUtil1 = []
AllUtil2 = []

# set the number of servers
Server_clean.SetUnits (9)
Server_load.SetUnits (2)
Server_oxidize.SetUnits (11)
Server_unload.SetUnits (2)

# set the run length and warmup period
RunLength = 5000
WarmUp = 0

def Release():
    if SimRNG.Uniform(0, 1, 3) <= 0.6: # p = 0.6, release type C product
        SimFunctions.Schedule(Calendar, "Release", 1)
        ProductC = SimClasses.Entity()
        ProductC.ClassNum = 1
        ProductC.Cycle = 0
        SimFunctions.SchedulePlus(Calendar, "Clean", 0.25, ProductC) # 0.25 hr = 15 minutes
    else: # p = 0.4, release type C product
        SimFunctions.Schedule(Calendar, "Release", 1)
        ProductD = SimClasses.Entity()
        ProductD.ClassNum = 2
        ProductD.Cycle = 0
        SimFunctions.SchedulePlus(Calendar, "Clean", 0.25, ProductD)

def Clean(Product):
    Queue_clean.Add(Product)
    if Product.Cycle == 0: #Product from release, first cycle
        if Server_clean.Busy < 9:
            Server_clean.Seize(1)
            NextProduct = Queue_clean.Remove() # customer leaves the queue if served
            SimFunctions.SchedulePlus(Calendar, "Load", SimRNG.Expon(1.822926, 2), NextProduct)
    else: #Product from Unload event, not first cycle
        Server_unload.Free(1)
        if Queue_unload.NumQueue() > 0:
            Server_unload.Seize(1)
            NextProduct = Queue_unload.Remove()  # customer leaves the queue if served

            if NextProduct.ClassNum == 1:
                if NextProduct.Cycle < 5:
                    SimFunctions.SchedulePlus(Calendar, "Clean", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
                else:
                    SimFunctions.SchedulePlus(Calendar, "EndOfProduction", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
            elif NextProduct.ClassNum == 2:
                if NextProduct.Cycle < 3:
                    SimFunctions.SchedulePlus(Calendar, "Clean", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
                else:
                    SimFunctions.SchedulePlus(Calendar, "EndOfProduction", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)


def Load(Product):
    Server_clean.Free(1)
    Queue_load.Add(Product)

    if Server_load.Busy < 2:
        Server_load.Seize(1)
        NextProduct = Queue_load.Remove() # customer leaves the queue if served
        SimFunctions.SchedulePlus(Calendar, "Oxidize", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
    if Queue_clean.NumQueue() > 0:
        Server_clean.Seize(1)
        NextProduct = Queue_clean.Remove()  # customer leaves the queue if served
        SimFunctions.SchedulePlus(Calendar, "Load", SimRNG.Expon(1.822926, 2), NextProduct)


def Oxidize(Product):
    Server_load.Free(1)
    Queue_oxidize.Add(Product)

    if Server_oxidize.Busy < 11:
        Server_oxidize.Seize(1)
        NextProduct = Queue_oxidize.Remove()  # customer leaves the queue if served
        if NextProduct.ClassNum == 1:
            SimFunctions.SchedulePlus(Calendar, "Unload", 2.7, NextProduct)
        elif NextProduct.ClassNum == 2:
            SimFunctions.SchedulePlus(Calendar, "Unload", 2, NextProduct)

    if Queue_load.NumQueue() > 0:
        Server_load.Seize(1)
        NextProduct = Queue_load.Remove() # customer leaves the queue if served
        SimFunctions.SchedulePlus(Calendar, "Oxidize", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)

def Unload(Product):
    Server_oxidize.Free(1)
    Queue_unload.Add(Product)
    Product.Cycle += 1
    if Server_unload.Busy < 2:
        Server_unload.Seize(1)
        NextProduct = Queue_unload.Remove()  # customer leaves the queue if served

        if NextProduct.ClassNum == 1:
            if Product.Cycle < 5:
                SimFunctions.SchedulePlus(Calendar, "Clean", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
            else:
                SimFunctions.SchedulePlus(Calendar, "EndOfProduction", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
        elif NextProduct.ClassNum == 2:
            if Product.Cycle < 3:
                SimFunctions.SchedulePlus(Calendar, "Clean", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
            else:
                SimFunctions.SchedulePlus(Calendar, "EndOfProduction", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)

    if Queue_oxidize.NumQueue() > 0:
        Server_oxidize.Seize(1)
        NextProduct = Queue_oxidize.Remove()  # Product leaves the queue if served
        if NextProduct.ClassNum == 1:
            SimFunctions.SchedulePlus(Calendar, "Unload", 2.7, NextProduct)
        elif NextProduct.ClassNum == 2:
            SimFunctions.SchedulePlus(Calendar, "Unload", 2, NextProduct)


def EndOfProduction(Product): # give an object to the EndOfProduction function to record total time in system
    Server_unload.Free(1)
    if Product.ClassNum == 1:
        TotalTime1.Record(SimClasses.Clock - Product.CreateTime) # Record the ProductC's total time in system
        AllMeanTC.append(TotalTime1.Mean())
    elif Product.ClassNum == 2:
        TotalTime2.Record(SimClasses.Clock - Product.CreateTime) # Record the ProductD's total time in system
        AllMeanTD.append((TotalTime2.Mean()))
    if Queue_unload.NumQueue() > 0:
        Server_unload.Seize(1)
        NextProduct = Queue_unload.Remove()  # customer leaves the queue if served

        if NextProduct.ClassNum == 1:
            if Product.Cycle < 5:
                SimFunctions.SchedulePlus(Calendar, "Clean", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
            else:
                SimFunctions.SchedulePlus(Calendar, "EndOfProduction", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
        elif NextProduct.ClassNum == 2:
            if Product.Cycle < 3:
                SimFunctions.SchedulePlus(Calendar, "Clean", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)
            else:
                SimFunctions.SchedulePlus(Calendar, "EndOfProduction", SimRNG.Erlang(2, 0.2377534 , 2), NextProduct)

# replication loop
for reps in range(0, 10, 1):

    SimFunctions.SimFunctionsInit(Calendar, TheQueues, TheCTStats, TheDTStats, TheResources)
    SimFunctions.Schedule(Calendar, "Release", 1)
    SimFunctions.Schedule(Calendar, "EndSimulation", RunLength)
    SimFunctions.Schedule(Calendar, "ClearIt", WarmUp)

    NextEvent = Calendar.Remove()
    SimClasses.Clock = NextEvent.EventTime
    if NextEvent.EventType == "Release":
        Release()
    elif NextEvent.EventType == "Clean":
        Clean(NextEvent.WhichObject)
    elif NextEvent.EventType == "Load":
        Load(NextEvent.WhichObject)
    elif NextEvent.EventType == "Oxidize":
        Oxidize(NextEvent.WhichObject)
    elif NextEvent.EventType == "Unload":
        Unload(NextEvent.WhichObject)
    elif NextEvent.EventType == "EndOfProduction":
        EndOfProduction(NextEvent.WhichObject)
    elif NextEvent.EventType == "ClearIt":
        SimFunctions.ClearStats(TheCTStats, TheDTStats)

    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        SimClasses.Clock = NextEvent.EventTime
        if NextEvent.EventType == "Release":
            Release()
        elif NextEvent.EventType == "Clean":
            Clean(NextEvent.WhichObject)
        elif NextEvent.EventType == "Load":
            Load(NextEvent.WhichObject)
        elif NextEvent.EventType == "Oxidize":
            Oxidize(NextEvent.WhichObject)
        elif NextEvent.EventType == "Unload":
            Unload(NextEvent.WhichObject)
        elif NextEvent.EventType == "EndOfProduction":
            EndOfProduction(NextEvent.WhichObject)
        elif NextEvent.EventType == "ClearIt":
            SimFunctions.ClearStats(TheCTStats, TheDTStats)

    # plot the mean cycle time for each product to determine the warmup period
    #plt.plot(range(0, int(TotalTime1.N())),AllMeanTC) # Mean Cycle time of product C vs number of Product C
    #plt.plot(range(0, int(TotalTime2.N())), AllMeanTD) # Mean Cycle time of product D vs number of Product D
    #plt.show()
    # Record the mean total time in system of each product
    AllTotalTime1.append(TotalTime1.Mean())
    AllTotalTime2.append(TotalTime2.Mean())
    print(AllTotalTime1[-1],AllTotalTime2[-1])

# Print the result of 95% CI
print("Estimate Long Run Time for product C is: ",t_mean_confidence_interval(AllTotalTime1,0.05))
print("Estimate Long Run Time for product D is: ",t_mean_confidence_interval(AllTotalTime2,0.05))
