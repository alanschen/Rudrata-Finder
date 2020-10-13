from DTHGraph import * 
from utils import *
from output_validator import *
import time
    
for i in range(1, 367):
    filename_in = "inputs/{}_200.in".format(i)
    print(filename_in)
    filename_out = "outputs/{}_200.out".format(i)
    DTHg = None
    try:
        DTHg = DTHGraph(filename_in)
    except:
        print("no input file called " + filename_in)
        continue
    
    t0 = time.time()
    try:
        DTHg.solve()
        print("Finished solving " + filename_in)
        t1 = time.time()
        t = np.round(t1 - t0, 2)
        DTHg.write_solution(filename_out)
        print("Successfully Generated in {} seconds ".format(t) + filename_in)
    except:
        t1 = time.time()
        t = np.round(t1 - t0, 2)
        DTHg.solution = [DTHg.start]
        DTHg.write_solution(filename_out)
    