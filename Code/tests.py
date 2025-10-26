from Posto import CaseStudy
import random
import math
from visualizer import *

cs = CaseStudy()

# Question 1
q0 = (random.uniform(0, 1), random.uniform(0, 1))
# print(cs.getTrajectory(q0, 10))
T = cs.getTrajectory(q0, 10)
plotTrajectory([T])


q0_bounds = ((0, 1), (0, 1))
#  Question 2 - Generating Logs
T = cs.getTrajectory(q0, 20)
log = cs.getLog(q0_bounds , trajectory = T , pr = 20 )
print("Uncertain Log :", log[0])
print("\nLog : ", log[1])



# Visualization of Random Trajectories
q0 = (random.uniform(0, 1), random.uniform(0, 1))
Ts = cs.getRandomTrajectories(q0_bounds, 100, 20)
plotTrajectory(Ts, arrow = False, random_color = True, show_point = False)


# Unsafe constraints
unsafe = 0.1
state = 0
op = 'ge'


# Plotting setting logging Probability as a variable
times = []
logProbs = []
colors = []


for i in range(1, 11):
    logP = i * 5
    tame, isSafe, valid, total = cs.checkSafe(q0_bounds, 2000, unsafe, state, op, pr = logP)

    invalid = total - valid

    if total == 0:
        color = (1, 0, 0)
    elif invalid > valid:
        color = (invalid / total, 0, 0)
    else:
        color = (0, valid / total, 0)


    times.append(tame)
    logProbs.append(logP)
    colors.append(color)




logProbTimeTRajC(logProbs, times, colors)    
    

# Plotting confidence vs time graph

safety = []
Cs = []
times = []

for i in range(1, 11):
    c = 0.1 * i if i != 10 else  0.1 * i - 0.01
    
    tame, isSafe, valid, total = cs.checkSafe(q0_bounds, 2000, unsafe, state, op, c = c)

    times.append(tame)
    Cs.append(c)
    safety.append(isSafe)


print(Cs)
TimevsC(Cs, times, safety)




    

