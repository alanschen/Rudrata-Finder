import numpy as np
import math
import networkx as nx
import time
from itertools import *
from input_validator import *
from output_validator import *
from utils import *
from student_utils import *
from rudrata import *
from general_solver import *

def convert_list(s):
    str1 = " "
    return (str1.join(s))

def write(lines, file_name):
    file = open(file_name,"w")
    for line in lines:
        line = line + "\n"
        file.write(line)

def write_line(locations, nodes):
    return [locations[n] for n in nodes]

class DTHGraph:
    solution = None
    dropoffs = None

    def __init__(self, file_name):
        """Sets up basic Information about the graph

        graph.labels = [all original labels with index = network x node number] (i.e graph.labels[0] == 'soda')

        graph.homes = [node numbers of homes] with len() = k

        graph.nxgraph = network x graph with number [1, 2, ..., n]

        graph.num_houses = number of TAs (k)
        
        graph.num_locs = number of locations (n)

        graph.dist = shorest all paths computed dynamically by floyd_warshall
        (i.e graph.dist[0][0] == 0)

        """
        data = read_file(file_name)
        parsed = data_parser(data)

        self.parsed = parsed

        self.num_locs = parsed[0]
        self.num_houses = parsed[1]
        self.labels = parsed[2]

        homes = parsed[3]
        start = parsed[4]
        matrix = parsed[5]

        self.homes = [self.labels.index(node) for node in homes]
        self.start = self.labels.index(start)

        self.nxgraph = adjacency_matrix_to_graph(matrix)[0]
        self.dist = nx.floyd_warshall(self.nxgraph)

    def named_path(self, path):
        """Covert networkx path to actual path"""
        return [self.labels[n] for n in path]

    def write_solution(self, file_name):
        """Write the solution if solution has been found into the file_name"""
        
        if self.solution != None:
            first_lines = []
            
            # line 1: the path of solution
            line1 = convert_list(self.named_path(self.solution))
            first_lines.append(line1)

            # find a dictionary mapping to where to drop off TAs
            self.map_dropoffs(self.solution)
            dropoffs = self.dropoffs

            # convert the dropoff location to strings of final lines
            
            
            if (self.solution[0] == self.solution[-1]):
                self.solution.pop()
            
            final_lines = []
            for stop in self.solution:
                # first add the stop label
                curr_line = [self.labels[stop]]
                curr_dropoffs = dropoffs[stop]
                # we add the tas location
                if len(curr_dropoffs) != 0:
                    for ta in dropoffs[stop]:
                        curr_line.append(self.labels[ta])
                # now we just convert the path
                if len(curr_line) != 1:
                    curr_line = convert_list(curr_line)
                    final_lines.append(curr_line)

            # write the lines in file
            result = first_lines + [str(len(final_lines))] + final_lines
            write(result, file_name)
        else:
            print("Graph has not been solved yet")

    def map_dropoffs(self, cycle):
        """Creates a dropoff dictionary for cost calculation"""
        dropoffs = {}
        for stop in cycle:
            dropoffs[stop] = []
        for n in self.homes:
            curr_stop = cycle[0]
            curr_min = self.dist[n][curr_stop]
            for stop in cycle:
                d = self.dist[n][stop]
                if d < curr_min:
                    curr_stop = stop
                    curr_min = d
            dropoffs[curr_stop].append(n)
        self.dropoffs = dropoffs

    def has_path(self, path):
        """Returns true is path is a path within this graph"""
        n, g = len(path), self.nxgraph
        for i in range(n - 1):
            u, v = path[i], path[i + 1]
            if not g.has_edge(u, v):
                print(u, v)
                return False
        return True

    def solve_rudrata(self, nodes=None, timeout=8):
        """Takes a set of nodes within this graph and finds a rudrata path using randomized algorithm
        If found, save to self.solutions and return None
        Otherwise, return None

        Default for nodes are self.homes + self.start (greedy approach)
        """
        def convert_to_sol(path, start):
            s = path.index(start)
            return path[s:] + path[:s] + [start]
        t0 = time.time()
        all_stops = nodes
        if all_stops == None:
            all_stops = self.homes[:]
            all_stops.append(self.start)
            
        stop_graph = self.nxgraph.subgraph(all_stops)
        path = rudrata_randomized(stop_graph, all_stops)
        while path == False:
            t1 = time.time()
            if t1 - t0 > timeout:
                return False
            path = rudrata_randomized(stop_graph, all_stops)
        sol = convert_to_sol(path, self.start)
        self.solution = sol

        return True


    def cycle_cost(self, cycle):
        """Takes a valid cycle and computes the cost of cycle"""
        self.map_dropoffs(cycle) # first compute the most optimal dropoff schedule
        return cost_of_solution(self.nxgraph, cycle, self.dropoffs)
    
    
    
    def solve(self):
        def has_uniform_edge_weight(self):
            G = self.nxgraph
            temp = list(G.edges(self.start))
            start_neighbor = temp[0][1]
            weight = G[self.start][start_neighbor]['weight']
            for edge in G.edges.data():
                if not (edge[2]['weight'] == weight):
                    return False
            return True
        
        if has_uniform_edge_weight(self):
            self.solve_rudrata()
        else: #graph doesnt have uniform edge weight (general graph) run Jinwei + nick's solver
            find_optimal(self)