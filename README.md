# Project: Pathfinding Robot from CS14003 of VNU-HCMUS
## Welcome
- Welcome to Project: Pathfinding Robot from CS14003: Introduction to Artificial Intelligence of VNU-HCMUS in little beautiful country named Viet Nam.

## Problem statement
Given a flat map $xOy$ (quadrant $I$), on which one places a starting point $S(x_S,y_S)$ and a destination point $G(x_G,y_G)$. At the same time, place obstacles as convex polygons so that the polygons are not placed on top of each other or have common points. The map space is limited to a rectangular frame with the lower left corner coinciding with the origin, the thickness of the frame is 1 unit. No point on the map may exceed or overlap this frame.
Choose and install algorithms to find the shortest path from $S$ to $G$ so that the path does not cut through polygons. The path can follow the edge of the polygon but must not overlap its edge. The graphical representation can be at its simplest level so that the user can see the polygons and paths.
The level of implementation is divided into the following levels:
- Level 1 (40%): successfully install an algorithm to find the path from $S$ to $G$. Report back on the algorithm and test run process. Note, test run if there is no road.
- Level 2 (30%): install at least 3 different algorithms (eg blind search, greedy, heuristic, ...). The report comments on the differences when testing three algorithms.
- Level 3 (20%): On the map, a number of other points will appear called pick-up points. Start from $S$, then go to pick up all these points and then reach state $G$. The order of pick-up points is not important. The goal is to find a way to minimize the total path. Report on the applied algorithm and the test run process.
- Level 4 (10%): polygons can move at speed $h$ (unit: $coordinates/s$). The simplest way to move can be to move back and forth a small distance to ensure it does not overlap other polygons. Run at least 1 algorithm on it. Record video and attach directly/link to the report.
- Level 5 (plus 10%): represents the model in 3-dimensional space (3D).

## How to run this project?
- To use this project, you first need to clone this project from the master branch of this GitHub repository [https://github.com/TheMetaSetter/pathfinding-robot/tree/master](https://github.com/TheMetaSetter/pathfinding-robot/tree/master)
## Clone this project from GitHub
### From your terminal
```git clone https://github.com/TheMetaSetter/pathfinding-robot```
### From this repo on browser
- Go to [https://github.com/TheMetaSetter/pathfinding-robot](https://github.com/TheMetaSetter/pathfinding-robot)
- Click on the green ```<> Code``` button and click ```Open with GitHub Desktop```. Make sure Github Desktop has been installed on your computer. If you haven't install it, follow instructions in this link [https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop](https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop)
- Finally, in the GUI of GitHub Desktop, open the repository in your favorite IDE or editor.
## Install dependencies
- In side the repo on your local machine, open the terminal and run ```pip install -r requirements.txt```.
## Run this project
- There are several files that you can run to test whether the project works properly.
- Run ```test_dijkstra_solver.py``` if you want to test the Dijkstra algorithm.
- Run ```test_a_asterisk_solver.py``` if you want to test the A-star algorithm.
- Run ```test_gbfs_solver.py``` if you want to test the GBFS algorithm.
- Run ```test_genetic_algorithm.py``` if you want to test the Genetic algorithm on TSP problem.
- Run ```evaluate_genetic_algorithm.py``` if you want to evaluate the performance of a set of parameters for Genetic algorithm.
- You can change the input of each script by modify the string passed to MapFileReader() constructor. For staic-obstacle TSP problem, the sample inputs are located inside the ```input_tsp``` directory. For the basic pathfinding problem, sample inputs are located inside ```input_basic``` directory. We have not implemented the dynamic-obstacle TSP problem, but the sample input for this problem is located in the file ```tsp_dynamic_obstacles.txt```.
