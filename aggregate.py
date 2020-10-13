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
import os 
import shutil

from DTHGraph import *

def copy_into(source_name, destination_name):
    if not os.path.exists(source_name):
        print("Input directory does not exist on {} ".format(source_name))
        return
    shutil.copyfile(source_name, destination_name)
    print("Copying from {} to {} complete".format(source_name, destination_name))

def choose_best(input_name, filenames):
    best_cost, index, costs = float('inf'), -1, []
    for i in range(len(filenames)):
        name = filenames[i]
        if not os.path.exists(name):
            continue
        cost = validate_output(input_name, name)[1]
        costs.append(np.round(cost, 2))
        if cost != 'infinite' and cost < best_cost:
            index = i
            best_cost = cost
    if index == -1:
        print("There are no valid solutions for {} ".format(input_name))
        return None
    print("Best output for {} is {}".format(input_name, filenames[index]))
    print("Costs for {} are {}".format(filenames, costs))
    return filenames[index]

input_directory = "inputs/"
output_directories = ["valid_outputs/", "nick_out/", "jinwei_out/"]
aggregate_directory = "outputs_aggregated/"


def aggregate_all(start, end, input_directory, output_directories, aggregate_directory):
    t0 = time.time()
    for i in range(start, end):
        for num in [50, 100, 200]:
            input_name = "{}{}_{}.in".format(input_directory, i, num)
            if not os.path.exists(input_name):
                print("{} does not exist".format(input_name))
                print("Success\n")
                continue
            filenames = ["{}{}_{}.out".format(instance, i, num) for instance in output_directories]
            
            best_filename = choose_best(input_name, filenames)
            if best_filename != None:
                output_filename = "{}{}_{}.out".format(aggregate_directory, i, num)
                print("Copying {} into {} ".format(best_filename, output_filename))
                copy_into(best_filename, output_filename)
                print("Success in {} seconds\n".format(np.round(time.time() - t0), 2))
                
aggregate_all(1, 370, input_directory, output_directories, aggregate_directory)
