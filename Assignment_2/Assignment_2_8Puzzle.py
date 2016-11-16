# A Python code for solving the 8-puzzle using A* and IDA* Search Methodology and comparing their efficiency under three different heuristics
# The heuristic 'a' says: h(n) = 0 i.e; A normal BFS
# The heuristic 'b' says: h(n) = Number of misplaced tiles or the Hamming Distance
# The heuristic 'c' says: h(n) = Sum of distances of the tiles from their goal positions
# 
# Code by: Mayank Roy | (github.com/mankeyboy) | 13CS30021 | AI Assignment 2 
# 
# 
# 
# 

#import statistics
import time
import math
import heapq
import random




def L(ePos):
    return ePos - 1
def R(ePos):
    return ePos + 1
def D(ePos):
    return ePos + 3
def U(ePos):
    return ePos - 3

def availActions(ePos):
    if ePos == 0 :
        return ['R','D']
    elif ePos == 1 :
        return ['L', 'D', 'R']
    elif ePos == 2 :
        return ['L', 'D']
    elif ePos == 3 :
        return [ 'U', 'D', 'R']
    elif ePos == 4 :
        return ['L', 'U', 'D', 'R']
    elif ePos == 5 :
        return ['L', 'U', 'D']
    elif ePos == 6 :
        return ['U', 'R']
    elif ePos == 7 :
        return ['L', 'U', 'R']
    elif ePos == 8 :
        return ['L', 'U']
        

def h(State,choice):
    cost = 0
    if choice == 'a' :
        return cost
    elif choice == 'b' :
        for i in range(len(State)) :       #Huerisitc B
            if State[i] != i and State[i] != 0 :
                cost += 1
    elif choice == 'c' :
        for i in range(len(State)):
            cost += (abs(i%3 - State[i]%3) + abs((i/3) - (State[i]/3)))
    return cost

def newState(oldState, action, ePos,gCost,choice):
    newS = oldState[:]
    if action == 'L' :
        newS[ePos],newS[L(ePos)] = oldState[L(ePos)],oldState[ePos]
        ePos -= 1
        gCost += 1
    elif action == 'R':
        newS[ePos],newS[R(ePos)] = oldState[R(ePos)],oldState[ePos]
        ePos += 1
        gCost += 1
    elif action == 'D':
        newS[ePos], newS[D(ePos)] = oldState[D(ePos)],oldState[ePos]
        ePos += 3
        gCost += 1
    elif action == 'U':
        newS[ePos], newS[U(ePos)] = oldState[U(ePos)],oldState[ePos]
        ePos -= 3
        gCost += 1
    fCost = gCost + h(newS,choice)
    # print newS, fCost
    s =(fCost,gCost,newS,ePos,oldState)
    return s

def checkIfGoal(State):
    for i in range(len(State[1:])):
        if State[i] != i :
            return False
    return True

def Solver(startState,choice):
    # print "Inside Solver"
    for i in range(len(startState)):
        if startState[i] == 0 :
            ePos = i
            break 
    nodesExpanded = 0
    if (checkIfGoal(startState)):
        return startState
    else :
        gCost = 0
        fCost = h(startState,choice) + gCost
        currentState = startState
        pQueue = []
        heapq.heappush(pQueue,(fCost,gCost,currentState,ePos,None))
        while True :
            currentState = heapq.heappop(pQueue)
            oldState = currentState[2]
            ePos = currentState[3]
            gCost = currentState[1]
            parent = currentState[4] 
            if(checkIfGoal(oldState)) :
                print "Nodes Expanded = %d" % nodesExpanded
                return currentState
            actions = availActions(ePos)
            nodesExpanded += 1
            for i in actions :
                newS = newState(oldState,i,ePos,gCost,choice)
                if newS[2] != parent :
                    heapq.heappush(pQueue,newS)
        

# if __name__ == '__main__':
#     print "Input the heuristic type : a/b/c"
#     choice = raw_input()
#     initialState = [[6,8,3,4,5,0,1,7,2],[1,5,7,8,3,6,2,0,4],[1,7,3,0,8,5,2,4,6],[0,4,7,8,6,1,3,2,5],[1,6,2,3,7,8,4,5,0],[8,2,6,7,1,5,3,4,0],[1,7,3,4,0,6,2,8,5],[4,2,6,8,3,5,0,7,1],[2,7,5,1,4,3,0,6,8],[4,7,8,1,3,0,6,2,5],[5,4,6,7,1,0,3,2,8],[7,5,3,4,8,2,0,1,6],[7,6,0,3,4,8,5,1,2],[5,6,1,8,0,7,3,2,4],[0,6,4,3,1,7,2,5,8],[6,0,5,2,4,7,3,8,1],[2,1,8,0,6,7,4,5,3],[1,5,2,0,6,8,7,3,4],[5,1,7,8,3,2,6,0,4],[1,3,0,5,2,4,6,8,7],[0,4,1,5,8,7,3,6,2],[2,8,7,5,6,0,1,3,4],[1,8,5,0,3,2,4,6,7],[8,3,4,5,6,7,2,0,1],[5,3,7,2,0,6,1,8,4],[2,6,5,3,8,0,1,4,7],[4,2,0,1,5,3,8,7,6],[7,3,4,8,6,5,2,1,0],[2,3,5,0,6,4,8,7,1],[1,0,8,4,7,2,3,5,6],[1,6,5,8,0,3,2,4,7],[8,6,1,5,2,3,7,4,0],[3,0,8,1,7,4,6,5,2],[2,1,0,3,4,5,7,6,8],[8,1,4,5,2,7,6,3,0],[1,2,8,3,6,7,5,0,4],[8,3,4,2,5,1,0,7,6],[0,5,6,8,2,4,1,3,7],[7,3,4,6,8,0,5,1,2],[8,1,5,0,6,3,7,2,4],[2,4,1,7,5,8,0,6,3],[2,6,1,8,3,4,7,0,5],[0,6,3,2,5,8,1,7,4],[1,4,0,2,7,6,5,3,8],[2,6,8,4,3,0,7,5,1],[5,4,2,3,8,1,6,7,0],[2,6,7,3,0,1,4,5,8],[7,3,4,0,6,8,1,2,5],[4,0,7,2,8,1,6,5,3],[6,7,5,0,3,4,1,2,8],[6,3,4,5,2,8,1,0,7],[8,4,0,1,3,5,7,2,6],[4,6,7,5,0,3,2,8,1],[5,0,8,1,4,3,6,2,7],[6,2,3,1,7,8,0,5,4],[2,5,1,0,8,4,3,7,6],[3,2,1,5,7,0,6,8,4],[5,1,2,0,8,6,4,7,3],[2,3,6,7,4,8,0,5,1],[4,8,0,1,5,3,2,6,7],[3,7,6,8,0,2,1,4,5],[0,1,4,6,5,3,2,7,8],[3,2,8,1,0,5,4,7,6],[2,6,7,4,1,0,3,8,5],[0,6,1,3,4,7,5,2,8],[5,2,0,6,8,3,1,7,4],[6,1,0,3,2,8,4,7,5],[8,2,6,0,3,5,7,4,1],[8,7,5,6,0,3,2,1,4],[5,0,1,3,2,4,8,7,6],[3,0,2,6,1,8,4,7,5],[7,6,1,4,0,2,5,3,8],[5,6,3,2,8,1,4,7,0],[8,5,0,2,3,1,4,7,6],[5,3,2,8,0,7,1,4,6],[5,8,1,2,7,4,3,6,0],[5,0,6,7,3,4,2,8,1],[6,5,0,2,8,3,4,1,7],[2,1,5,6,4,3,0,7,8],[5,3,8,0,2,6,4,7,1],[1,8,0,4,2,7,5,3,6],[2,8,4,0,5,3,6,7,1],[8,5,7,4,3,1,0,6,2],[2,6,8,0,3,5,1,7,4],[5,2,0,8,6,7,4,1,3],[5,1,6,3,4,0,8,7,2],[2,7,8,0,5,1,4,6,3],[5,1,7,2,3,4,6,8,0],[2,1,3,8,7,0,5,6,4],[7,1,3,8,2,0,4,6,5],[2,3,7,5,0,6,8,1,4],[0,2,8,7,5,4,6,3,1],[5,3,1,4,7,0,6,2,8],[4,6,2,5,3,8,0,7,1],[7,0,8,5,6,4,2,1,3],[4,7,8,1,0,5,2,6,3],[5,4,6,1,3,8,7,0,2],[7,6,5,8,1,0,2,4,3],[1,7,2,8,4,6,3,0,5],[2,8,5,1,6,4,7,3,0]]
#     # initialState = [[1,4,0,3,7,2,6,8,5]]
#     if(len(choice) > 1 or choice > 'c'):
#         print "Wrong Input/ No such heuristic"
#     else :
#         for i in range(len(initialState)) : 
#             solN = Solver((initialState[i]),choice)
#             print "Initial State, f(n)"
#             print initialState[i] , solN[0]


