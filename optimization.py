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
from network import SFC, Topo_SFC

def mapping(sfc,topo):
    num_vnfs = sfc.get_num_nodes()
    num_vnf_links=sfc.get_num_links()
    
    num_nodes = topo.get_num_nodes()
    num_links =topo.get_num_links()
    
    #mapping node variable
    x=cp.Variable((num_vnfs,num_nodes),boolean=True)
    #mapping link variable
    y=cp.Variable((num_vnf_links, num_links),boolean=True)
    
    #array of nodes
    list_of_nodes= topo.G.nodes()
    list_node_caps=topo.get_array_node_cap()
    list_link_bws=topo.get_array_link_bw()
    #array cap of nodes
    list_of_vnfs = sfc.G.nodes()
    list_vnf_caps= sfc.get_array_vnf_cap()
    list_vnf_bws=sfc.get_array_link_bw()
    
    #price of node
    node_prices=[]
    for n in topo.G.nodes(data=True):
        node_prices.append(n[1]['res'])
    #print("price",node_prices)
    #check constraint capacity
    constraints=[]
    
    for i in range(num_nodes):
        cap =0
        for j in range(num_vnfs):
            cap+=x[j,i]*list_vnf_caps[j]
            
        constraints+=[cap<=list_node_caps[i]]
    
    for i in range(num_vnfs):
        constraints+=[sum(x[i,:])==1 ]
    #check link bw constraint
    
    for i in range(num_links):
        bw =0
        for j in range(num_vnf_links):
            bw=bw+y[j,i]*list_vnf_bws[j]
        constraints+=[bw<=list_link_bws[i]]
    
    total_price=0
    for i in range(num_vnfs):
        for j in range(num_nodes):
            total_price+=x[i,j]*node_prices[j]
            
    obj=cp.Minimize(total_price)
    problem = cp.Problem(obj,constraints)
    problem.solve(qcp=True)
    print("Mapping solution",x.value)

    # for i in range(num_vnfs):
    #     for j in range(num_nodes):
    #         print('% 6.2f' % x.value[i,j])
    #print(problem)

    
    plt.show()

sfc= SFC()
sfc.printSFC()
tp =Topo_SFC()
mapping(sfc, tp)
sfc= SFC([4,5,6],[1,2,2],[(4,5),(4,6)],[30,20])
sfc.printSFC()
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