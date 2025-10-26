# Introduction

This is a project which uses the tool called ['Posto'](https://github.com/bineet-coderep/posto/tree/main) to monitor a system.

The paper [link](https://dl.acm.org/doi/10.1007/978-3-031-95497-9_7).

# Problem Statement

Given a non-linear I/0 system. Perform monitoring with confidence $c$.
The system is defined as :

$$ x_[i + 1] = x_i - d t(y_i + 1.5x_i + 1.5x_i^2)  $$
$$ y_[i + 1] = y_i + d t (3x_i^2 - y_i) $$


# Files

1. `Posto.py` - Contains the class which has functions to generate and validate logs and trajectories.
2. `visualizer.py` - Used to plot diagrams in the Presentation.
3. `results.py` - Used to generate results and diagrams.

# Results

The results are present in the presentation.
