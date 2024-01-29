def updateQueue(processQueue, currentTime, arrivalTimes, numProcesses, maxProcessIndex):
    zeroIndex = -1
    for i in range(numProcesses):
        if processQueue[i] == 0:
            zeroIndex = i
            break

    if zeroIndex == -1:
        return

    processQueue[zeroIndex] = maxProcessIndex + 1


def checkNewArrival(currentTime, arrivalTimes, numProcesses, maxProcessIndex, processQueue):
    if currentTime <= arrivalTimes[numProcesses - 1]:
        newArrival = False
        for j in range(maxProcessIndex + 1, numProcesses):
            if arrivalTimes[j] <= currentTime:
                if maxProcessIndex < j:
                    maxProcessIndex = j
                    newArrival = True

        if newArrival:
            updateQueue(processQueue, currentTime, arrivalTimes, numProcesses, maxProcessIndex)


def maintainQueue(processQueue, numProcesses):
    for i in range(numProcesses - 1):
        if processQueue[i + 1] != 0:
            processQueue[i], processQueue[i + 1] = processQueue[i + 1], processQueue[i]


currentTime, maxProcessIndex = 0, 0
avgWait, avgTurnaroundTime = 0, 0

print("\nPlease enter the time quantum:", end=" ")
timeQuantum = int(input())
print("\nPlease enter the number of processes: ", end=" ")
numProcesses = int(input())
arrivalTimes = [0] * numProcesses
burstTimes = [0] * numProcesses
waitingTimes = [0] * numProcesses
turnaroundTimes = [0] * numProcesses
completionTimes = [0] * numProcesses
processQueue = [0] * numProcesses
tempBurstTimes = [0] * numProcesses
completedProcesses = [False] * numProcesses

# User input for context switch time
print("\nPlease enter the context switch time: ", end=" ")
contextSwitchTime = int(input())

for i in range(numProcesses):
    print(f"Enter arrival time for PID {i + 1}: ", end="")
    arrivalTimes[i] = int(input())

for i in range(numProcesses):
    print(f"Enter burst time for PID {i + 1}: ", end="")
    burstTimes[i] = int(input())
    tempBurstTimes[i] = burstTimes[i]

for i in range(numProcesses):
    completedProcesses[i] = False
    processQueue[i] = 0

while currentTime < arrivalTimes[0]:
    currentTime += 1

processQueue[0] = 1

while True:
    flag = True
    for i in range(numProcesses):
        if tempBurstTimes[i] != 0:
            flag = False
            break

    if flag:
        break

    for i in range(numProcesses and processQueue[i] != 0):
        ctr = 0
        while ctr < timeQuantum and tempBurstTimes[processQueue[0] - 1] > 0:
            tempBurstTimes[processQueue[0] - 1] -= 1
            currentTime += 1
            ctr += 1

            checkNewArrival(currentTime, arrivalTimes, numProcesses, maxProcessIndex, processQueue)

        if tempBurstTimes[processQueue[0] - 1] == 0 and not completedProcesses[processQueue[0] - 1]:
            turnaroundTimes[processQueue[0] - 1] = currentTime
            completionTimes[processQueue[0] - 1] = currentTime
            completedProcesses[processQueue[0] - 1] = True

        idle = True
        if processQueue[numProcesses - 1] == 0:
            for k in range(numProcesses):
                if processQueue[k] != 0:
                    if not completedProcesses[processQueue[k] - 1]:
                        idle = False
        else:
            idle = False

        if idle:
            currentTime += contextSwitchTime
            checkNewArrival(currentTime, arrivalTimes, numProcesses, maxProcessIndex, processQueue)

        maintainQueue(processQueue, numProcesses)

for i in range(numProcesses):
    turnaroundTimes[i] = turnaroundTimes[i] - arrivalTimes[i]
    waitingTimes[i] = turnaroundTimes[i] - burstTimes[i]

print("\nPID.\tArrival Time\tBurst Time\tCompletion Time  \tWait Time\tTurnaround Time\n")

for i in range(numProcesses):
    print(f"{i + 1}\t\t{arrivalTimes[i]}\t\t{burstTimes[i]}\t\t{completionTimes[i]}\t\t{waitingTimes[i]}\t\t{turnaroundTimes[i]}\n")

# Change the types to float for average calculations
avgWait = 0.0
avgTurnaroundTime = 0.0

for i in range(numProcesses):
    avgWait += waitingTimes[i]
    avgTurnaroundTime += turnaroundTimes[i]

avgWait /= numProcesses
avgTurnaroundTime /= numProcesses

print("\nAverage wait time : ", avgWait)
print("\nAverage Turnaround Time : ", avgTurnaroundTime)
