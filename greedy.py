import numpy as np
import math
import networkx as nx
import time
import random
from itertools import *
from input_validator import *
from output_validator import *
from utils import *
from student_utils import *
from rudrata import *
from general_solver import *

from DTHGraph import *

def do_for_all():
    for i in range(1, 368):
        for size in [50, 100, 200]:
            input_name = "inputs/{}_{}.in".format(i, size)
            output_name = "valid_outputs/{}_{}.out".format(i, size)
            DTHg, greedy_cost = None, float('inf')
            try:
                DTHg = DTHGraph(input_name)
            except:
                print("No input file called " + input_name)
                continue
                
            greedy_solver(DTHg)
            greedy_cost = DTHg.cycle_cost(DTHg.solution)[0]
            g = DTHg
            
            cost = float('inf')
            if os.path.exists(output_name):
                try:
                    cost = validate_output(input_name, output_name)[1]
                    if cost == 'infinite' or cost > greedy_cost:
                        print("Case Better: Writing new solution to " + output_name)
                        g.write_solution(output_name)
                    else:
                        print("Case Not as good: we keep previous solution")
                except:
                    print("Case Failed: Writing new solution to " + output_name)
                    g.write_solution(output_name)
            else:
                print("Case DoesNotExist: Writing new solution to " + output_name)
                g.write_solution(output_name)
            
            if cost != 'inf':
                print("Correct output with cost {} ".format(np.round(cost, 2)) + output_name + "\n")
            else:
                print("WARNING: " + output_name + "\n")

def time_since(t0):
    now = time.time()
    return np.round(now - t0, 2)

def greedy_solver(DTHGraph, timeout=40):
    def path(u, v):
        return nx.reconstruct_path(u, v, predecessors)
    t0, curr_min = time.time(), float('inf')
    solution = []
    predecessors, _ = nx.floyd_warshall_predecessor_and_distance(DTHGraph.nxgraph)
    solution.append(DTHGraph.start)
    curr_loc = DTHGraph.start
    remaining_loc = DTHGraph.homes[:]
    
    while len(remaining_loc) != 0:
        distances = [DTHGraph.dist[curr_loc][v] for v in remaining_loc]
        best = remaining_loc.pop(np.argmin(distances))
        if best == curr_loc:
            continue
        walk = path(curr_loc, best)
        solution += walk[1:]
        curr_loc = best
    
    walk = path(curr_loc, DTHGraph.start)
    solution += walk[1:]
                     
    DTHGraph.solution = solution
    
do_for_all()
