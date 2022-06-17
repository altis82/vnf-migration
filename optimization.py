#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 12:22:16 2022

@author: admin
"""

import numpy as np
import networkx as nx
import pickle
import cvxpy as cp
from scipy.spatial import distance_matrix
#import gurobi as gr
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt


def mapping(sfc,topo):
    
    x=cp.Variable(num_vnfs,num_nodes)
    pass
###########################3
# r=cp.Variable(num_paths,pos=True)
# constraints=[]
# #check the link capacity of each path
# list_min_bw_paths=[]
# list_delay_paths=[]
# for path in listpath:
#     i=0
#     list_min_bw_paths.append(self.get_min_bw_of_path(path))
#     list_delay_paths.append(self.get_latency_of_path(path))
#     constraints+=[r[i]<=list_min_bw_paths[i]]
#     i+=1
# #print(len(list_delay_paths),num_paths)
# obj=cp.Minimize(cp.sum(list_delay_paths*r))

# constraints+=[cp.sum(r)==request_rate]
# problem = cp.Problem(obj, constraints)
# #print(problem)
# problem.solve(qcp=True)
# #print('value:',r.value)