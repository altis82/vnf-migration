#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:35:03 2022

@author: admin
"""

import gurobipy as gp
from gurobipy import GRB

import cvxpy as cp
import numpy as np
import networkx as nx
import pickle
import cvxpy as cvx
from scipy.spatial import distance_matrix
#import gurobi as gr
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from network import Topo_SFC as Topo_SFC

MAXLINKCAP=1 #Gbps
MAXLATENCY=10 #ms
MAx_USERS_BS1=200
MAx_USERS_BS2=200
MAx_USERS_BS3=200
#create a network node
num_nodes = 6
num_links = 7
link_bandwidths =[[0,       1000    ,0      ,2000  ,0  ,0],
                  [1000,    0       ,1000   ,0     ,0  ,0],
                  [0        ,1000  ,0      ,1000,  0,  1500],
                  [2000,    0      ,1000,  0,     2000, 0   ],
                  [0,       0,      0,      2000,   0,  2000],
                  [0,       0,      1500,   0,  2000,   0]
                  ]


#def routing_path(self,src,des,request_rate):
tp_network = Topo_SFC()
tp_network.draw_network()
tp_network.routing_path(1, 4, 30)
