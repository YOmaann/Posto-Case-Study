import os,sys,copy
import time

PROJECT_ROOT = os.environ['MNTR_BB_ROOT_DIR']
sys.path.append(PROJECT_ROOT)

from Parameters import *
from lib.GenLog import *
from lib.TrajValidity import *
from lib.TrajSafety import *
from lib.JFBF import *
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import random

class CaseStudy:

    # Given state q return next state _q
    def nextState(self, q):
        delta = DT
        ep = DELTA_STATE

        # Current coordinates
        x = q[0]
        y = q[1]

        # Add noise
        x += random.uniform(0, ep)
        y += random.uniform(0, ep)

        #  Calculate next x and y
        _x = x + delta * (-y * 1.5 * x - 1.5 * x * x)
        _y = y + delta * (3 * x * x - y)

        _q = (_x, _y)
        return _q


    # Generate trajectory of length T
    def getTrajectory(self, q0, T):
        path = [] # Path
        cur_q = copy.copy(q0)

        for t in range(T):
            path.append(cur_q)
            cur_q = self.nextState(cur_q)

        # Return path
        return path

    # Get K random trajectories of length T
    # Here q0 \subseteq Q where Q is the set of all states.
    def getRandomTrajectories(self, q0, T, K):
        trajs = []

        for i in range(K):
            # Get a random initial state from the set of initial states
            x0 = random.uniform(q0[0][0], q0[0][1])
            y0 = random.uniform(q0[1][0], q0[1][1])

            q = (x0, y0)
            trajectory = self.getTrajectory(q, T)
            trajs.append(trajectory)

        # Return trajectory
        return trajs


    # Get a log of based on a trajectory T
    def getLog(self, q0, trajectory = None, T = 10, pr = PROBABILITY_LOG):
        # Get one random trajectory starting from an inital state.
        if not trajectory:
            trajectory = self.getRandomTrajectories(q0, T, 1)[0]

        logger = GenLog(trajectory)
        log = logger.genLog(pr = pr)

        # Log is a tuple of size 2
        return log


    # Generate K valid trajectories
    # Given a log 'logUn' return the list of K valid trajectories
    # The definition of valid trajectories follow
    # 
    
    def getValidTrajectories(self, q0, T, K, logUn):
        validTrajectoryO = TrajValidity(logUn)
        validT = []

        while len(validT) <= K:
            # Generate 1 random trajectory
            trajectory = self.getRandomTrajectories(logUn[0][0], T, 100)
            valid_ts , _ = validTrajectoryO.getValTrajs()

            validT = validT + valid_ts[0:K - len(valid_ts)]

        
    # JFB in the tool (Jeffries Bayes Factor) calculates K and error values based on the paper.
    # Step 1 : Get random trajectories.
    # Step 2 : Get logs from them with over approximation.
    # Step 3 : Get values of K (JFB values).
    # Step 4 : Gte safe and unsafe records from the log.
    # Step 5 : if unsafe records > 0  then  the system is unsafe RETURN.
    # Step 6 : fill in the valid trajectories list.
    # Step 7 : Get 100 reandom trajectories
    # Step 8 : Filter valid trajectories from them.
    # Step 9 : Add valud trajectories to the safe list.
    # Step 10 : if any one valid trajectory is unsafe. return false and break.
    # Step 11 : return True.
        
    def checkSafe(self, q0, T, unsafe, state, op, logging = True, pr = PROBABILITY_LOG, c = c):
        # This code is copied from the original source Jet.py
        ts=time.time()
        trajsL=self.getRandomTrajectories(q0,T,1)
        logger=GenLog(trajsL[0])
        logUn=logger.genLog(pr = pr)[0]
        K=JFB(B,c).getNumberOfSamples()
        isSafe=True
        totTrajs=0
        valTrajObj=TrajValidity(logUn) # 
        valTrajs=[] # Set of valid trajectories
        safeTrajs=[] # Set of safe trajectories
        unsafeTrajs=[] # Set of unsafe trajectories
        safeTrajObj=TrajSafety([state,op,unsafe])
        (safeSamps,unsafeSamps)=safeTrajObj.getSafeUnsafeLog(logUn)
        if len(unsafeSamps)==0:
            while len(valTrajs)<=K:
                # Generate 100 trajectories at the same time
                trajs=self.getRandomTrajectories(logUn[0][0],T,100)
                totTrajs+=1
                valTrajsIt,inValTrajsIt=valTrajObj.getValTrajs(trajs)
                print(totTrajs*100,len(valTrajs))
                # Check safety of valTrajsIt
                (safeTrajs,unsafeTrajs)=safeTrajObj.getSafeUnsafeTrajs(valTrajsIt)
                if len(unsafeTrajs)>0:
                    isSafe=False
                    break

                valTrajs=valTrajs+valTrajsIt
                if len(valTrajs)>=K:
                    break
        else:
            isSafe=False
        
        ts=time.time()-ts

        if logging:
            print("Time Taken: ",ts)
            print("Safety: ",isSafe)
            print("[Trajs] Safe, Unsafe: ",len(safeTrajs),len(unsafeTrajs))
            print("[Log] Safe, Unsafe: ",len(safeSamps),len(unsafeSamps))
            print("Total Trajectories Generated: ",totTrajs*100,"; Valid Trajectories: ",len(valTrajs))

        # Time , Safety, len(valid Trajectories), len(total Trajectories)
        return (ts, isSafe, len(valTrajs), totTrajs * 100)

        


# x_init=0.8
# y_init=0.8
# T=2000

# unsafe=-0.30
# state=0
# op='le'

# initState=(x_init,y_init)
# initSet=([0.8,1],[0.8,1])

# cs = CaseStudy()
# cs.checkSafe(initSet,T,unsafe,state,op)
