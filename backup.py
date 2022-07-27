#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 14:44:59 2022

@author: admin
"""

import numpy as np
import math
import matplotlib.pyplot as plt

#define network topology
num_nodes=5
#matrix bandwidth connections
# connect_nodes=np.zeros((num_nodes,num_nodes))

# for n in range(num_nodes-1):
#     m=n+1
#     while m<num_nodes:
#         if n!=m:
#             tmp=np.random.choice([0,10,20,30,40])
#             connect_nodes[n,m]=tmp
#             connect_nodes[m,n]=tmp
#         m=m+1
    
connect_nodes=[[ 0., 30., 20., 30., 30.],
 [30.,  0.,  0., 10., 30.],
 [20.,  0.,  0., 40.,  0.],
 [30., 10., 40.,  0., 20.],
 [30., 30.,  0., 20.,  0.]]
print("Matrix BW:", connect_nodes)
resource_nodes=[100]*num_nodes

#define SFC
num_vnfs=3
#matrix bandwith connections
connect_vnfs=[[0,10,0],
              [10,0,20],
              [0,20,0]]
#placement
placement=np.zeros((num_nodes,num_vnfs))
placement=[[1,0,0],
          [0,1,1],
          [0,0,0]
          ]

N = 1000
d = 10

#reward_list=[0,3,3,3,4,5,4,5,4,3]

def MAB(N_arms, reward_list):
    arms_selected=[]
    d=N_arms
    N_selections=[0]*d
    sum_rewards=[0]*d
    avg_reward=0
    #for reach round
    for n in range(N):
        arm=0
        max_upper_bound=0
        for i in range(N_arms):
            if N_selections[i]>0:
                avg_reward=sum_rewards[i]/N_selections[i]
                tmp_i=math.sqrt(3/2*math.log(n+1)/N_selections[i])
                upper_bound=avg_reward+tmp_i
            else:
                upper_bound=1e40
            if upper_bound>max_upper_bound:
                max_upper_bound=upper_bound
                arm=i
                
        arms_selected.append(arm)
        N_selections[arm]=N_selections[arm]+1
        #get reward when selecting an arm
        reward=reward_list[arm]
        sum_rewards[arm]=sum_rewards[arm]+reward
        #total_reward = total_reward+reward
            
    print("selected arms:",reward_list)
    print("selection",N_selections)
MAB(d,reward_list)
    

