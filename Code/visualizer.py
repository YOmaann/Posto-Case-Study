import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import random
from mpl_toolkits.mplot3d import Axes3D

def plotTrajectory(taus, arrow = True, random_color = False, show_point = True):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    
    for i, tau in enumerate(taus):
        x, y = list(zip(*tau))
        z = list(range(len(x)))

        color = 'blue'
        
        if random_color:
            color = (random.uniform(0,1), random.uniform(0,1), random.uniform(0,1), 1)
            
        ax.plot(x, y, z, color=color, linewidth=2, label=f'Trajectory {i + 1}')

        if show_point:
            ax.scatter(x, y, z, color=color, s=40)

        if not arrow:
            continue
        
        for i in range(len(x) - 1):
            marker_pos = 0.8
            x_marker = x[i] + marker_pos * (x[i+1] - x[i])
            y_marker = y[i] + marker_pos * (y[i+1] - y[i])
            z_marker = z[i] + marker_pos * (z[i+1] - z[i])
        
            ax.scatter([x_marker], [y_marker], [z_marker], 
                       color='red', marker='>', s=100, edgecolors='black')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('T')
    ax.set_title('Random Trajectory')
    ax.legend()
    plt.show()


def logProbTimeTRajC(logProbs, times, colors):
    plt.scatter(logProbs, times, c = colors)

    plt.xlabel("Logging Probability")
    plt.ylabel("Time")
    plt.title("Time and safety")

    plt.show()


def TimevsC(cs, times, safety):
    plt.plot(cs, times, color='blue', linewidth=1)

    for c, time, safe in zip(cs, times, safety):
        if safe:
            plt.scatter(c, time, c = 'green')
        else:
            plt.scatter(c, time, c = 'red')

    plt.xlabel("Confidence 'c'")
    plt.ylabel("Time")
    plt.title("Time vs Confidence")

    plt.show()

    
# ==================================================
