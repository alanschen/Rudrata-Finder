# Rudrata-Finder
Rudrata Path Finder approximating ride-share problems such as Uber Pool. Capping project for CS 170: Efficient Algorithms and Complexity Theory

## Rudrata.py
A randomized hamiltonian path finder that finds rudrata path with certain probability, assuming it has one. The approach is similar to the game nibble/snake (or just slither.io) where we simply DFS the graph except we explore with additional rule for probability to visit nodes that we have already visited before. The algorithm exits after a certain number of tries (if the initial visits of the explore is a deadend, we could be stuck). So we run the algorithm multiple times with random restarts and random reversal in addition to exploring. Empirically, we found that most graphs that are reasonably connected will return a rudrata path within one to two seconds.

## Greedy.py
A simple greedy algorithm that always picks the nearest location to drive to from the current location starting with starting point. First computing all paths using floyd-warshall algorithm, then use that as a linear time mapping to construct the solution.

## Aggregate.py
This file takes in a number of directories and searches for possible .out files, compares solution and their costs, picks the best one and writes into another directory. In our solution, we aggregated greedy outcome with our algorithms.

## DTHGraph.py
This file acts as a wrapper for our graphs. We used this class to create our own graph class that has sub methods commonly used in our algorithm. The initialization method takes in a file name (for example 1_50.in) and parses the input file to create a networkx graph and other instance variables like homes, num_homes, locations, num_locations. The highest level method is DTHGraph.solve which solves the graph depending if the graph has uniform edge weights or not. If the graph has uniform edge weight we use DTHGraph.solve_rudrata which calls rudrata_randomized inside rudrata.py on a subset of the nodes on the networkx graph.
