#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 11:22:45 2021

@author: admin
"""
#source ~/anaconda3/bin/activate root

import cvxpy as cp
import numpy as np
import networkx as nx
import pickle

from scipy.spatial import distance_matrix
#import gurobi as gr
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt

MAXLINKCAP=1 #Gbps
MAXLATENCY=10 #ms
MAx_USERS_BS1=200
MAx_USERS_BS2=200
MAx_USERS_BS3=200


######

######

class SFC:
    #args: list of nodes, list of res, list of connections
    #example: [1,2,3],[1,2,1],[(1,2),(2,3)],[10,20]
    def __init__(self, *args):
        if len(args)<1:
            self.G= nx.Graph()
            self.G.add_node(0, color='yellow',res=1)
            self.G.add_node(1, color='yellow', res=2.5)
            self.G.add_node(2, color='yellow', res =3)
            
            self.G.add_edge(0,1, bw=10)
            self.G.add_edge(1,2, bw=20)
        else:
            self.G=nx.Graph()
            #add nodes
            for i in range(len(args[0])):
                self.G.add_node(args[0][i], color='yellow', res=args[1][i])
            #add links and bandwidths
            for i in range(len(args[2])):
                self.G.add_edge(args[2][i][0],args[2][i][1],bw=args[3])
    def printSFC(self):
        strsfc="SFC:"
        k=self.G.number_of_nodes()
        i=1
        for n in self.G.nodes(data=True):
            strsfc=strsfc+str(n[0])
            if i<k:
                strsfc+=","
            i=i+1
        
            
        print(strsfc)
        
    def get_num_nodes(self):
        return self.G.number_of_nodes()
    
    def get_array_vnf_cap(self):
        list_node_cap=[]
        for n in self.G.nodes(data=True):
            #print("res",n[1]['res'])
            list_node_cap.append(n[1]['res'])
        return list_node_cap
    
    
    def get_array_link_bw(self):
        list_link_bws=[]
        for l in self.G.edges(data=True):
            #print(l)
            list_link_bws.append(l[2]['bw'])
        return list_link_bws
    
    def get_num_links(self):
        return self.G.number_of_edges()
        
class Topo_SFC:
    def __init__(self):
        self.G = nx.Graph()
        self.G.add_node(0,color='red',res=10)
        self.G.add_node(1,color='red', res =5)
        self. G.add_node(2,color='red', res =6)
        #BSs
        self.G.add_node(3,color='yellow', res =5)
        self.G.add_node(4,color='yellow', res =25)
        self.G.add_node(5,color='yellow', res =25)
        self.G.add_node(6,color='yellow', res =25)
        #switches
        self.G.add_node(7,color='blue', res =25)
        self.G.add_node(8,color='blue', res =25)
        self.G.add_node(9,color='blue', res =25)
        self.G.add_node(10,color='blue', res =16)
        self.G.add_node(11,color='blue', res =12)
        self.G.add_node(12,color='blue', res =21)
        self.G.add_node(13,color='blue', res =20)
        #core nodes
        self.G.add_node(14,color='blue', res =200)
        self.G.add_node(15,color='blue', res =255)
        self.G.add_node(16,color='blue', res =125)
        self.G.add_node(17,color='blue', res =250)
        self.G.add_node(18,color='blue', res =100)
        self.G.add_node(19,color='blue', res =252)
        self.G.add_node(20,color='blue', res =250)
    
        self.G.add_edge(0,1,bw=1000)
        self.G.add_edge(0,2,bw=1000)
        self.G.add_edge(0,4,bw=1000)
        self.G.add_edge(0,10,bw=1000)
        self.G.add_edge(1,6,bw=120)
        self.G.add_edge(1,3,bw=50)
        self.G.add_edge(1,7,bw=60)
    
        self.G.add_edge(2,8,bw=150)
        self.G.add_edge(2,9,bw=120)
    
        self.G.add_edge(4,8,bw=60)
    
        self.G.add_edge(5,8,bw=90)
        self.G.add_edge(5,9,bw=100)
    
        self.G.add_edge(6,7,bw=100)
        self.G.add_edge(6,10,bw=200)
    
        self.G.add_edge(9,10,bw=60)
        self.G.add_edge(9,12,bw=60)
        self.G.add_edge(9,13,bw=50)
        self.G.add_edge(9,16,bw=100)
    
        self.G.add_edge(10,11,bw=40)
        self.G.add_edge(10,12,bw=50)
    
        self.G.add_edge(11,14,bw=60)
    
        self.G.add_edge(12,13,bw=60)
    
        self.G.add_edge(15,16,bw=90)
        self.G.add_edge(16,17,bw=80)
        self.G.add_edge(16,18,bw=70)
        self.G.add_edge(17,18,bw=120)
        self.G.add_edge(17,19,bw=60)
        self.G.add_edge(18,20,bw=160) 
    
    
        self.pos = nx.spring_layout(self.G)
    
        #output=open('graph.p', "wb" )
        #pickle.dump(self.pos,output)
        try:
            output=open('graph.p', "rb" )
            self.pos=pickle.load(output)
        except:
            output=open('graph.p', "wb" )
            pickle.dump(self.pos,output)
            
        
        
        #draw_network(G)
    
    def get_array_link_bw(self):
        list_link_bws=[]
        for l in self.G.edges(data=True):
            #print(l[2]['bw'])
            list_link_bws.append(l[2]['bw'])
        return list_link_bws
   
    def get_array_node_cap(self):
        list_node_cap=[]
        for n in self.G.nodes(data=True):
            #print("res",n[1]['res'])
            list_node_cap.append(n[1]['res'])
        return list_node_cap
    
    def get_num_nodes(self):
        return self.G.number_of_nodes()
    
    def get_num_links(self):
        return self.G.number_of_edges()
    
    def draw_network(self):    
        
        nx.draw_networkx_nodes(self.G, self.pos,node_size=120)
        nx.draw_networkx_labels(self.G, self.pos)
        nx.draw_networkx_edges(self.G, self.pos, edge_color='r', arrows = False)    
        
        coords=[]
        for n in self.G.nodes():
            coords.append(self.pos[n])    
    
        plt.show();
        return coords
    
    def get_link_of_path(self, path):
        list_of_link=[]
        for i in range(len(path)):
            if i <len(path)-1:
                link=(path[i],path[i+1])
                list_of_link.append(link)
        
        return list_of_link

    def get_latency_of_path(self,path):
        delay=0
        for i in range(len(path)):
            if i <len(path)-1:
                link=(path[i],path[i+1])
                delay+=1000./self.G[path[i]][path[i+1]]['bw']
        return delay
    
        
    def get_min_bw_of_path(self, path):
        minbw=10000
        min_link=()
        for i in range(len(path)):
            if i<len(path)-1:
                if self.G.has_edge(i,i+1):
                    bw=self.G[path[i]][path[i+1]]['bw']
                    if bw<minbw:
                        minbw=bw
                        min_link=(path[i],path[i+1])
        return minbw
    def routing_user():
        # Problem data
        n = 5                     # number of transmitters and receivers
        m=3#number of BSs
        sigma = 0.5 * np.ones(n)  # noise power at the receiver i
        p_min = 0.1 * np.ones(n)  # minimum power at the transmitter i
        p_max = 5 * np.ones(n)    # maximum power at the transmitter i
        sinr_min = 0.2            # threshold SINR for each receiver
        
        # Path gain matrix
        G = np.array(
           [[1.0, 0.1, 0.2, 0.1, 0.05],
            [0.1, 1.0, 0.1, 0.1, 0.05],
            [0.2, 0.1, 1.0, 0.2, 0.2],
            [0.1, 0.1, 0.2, 1.0, 0.1],
            [0.05, 0.05, 0.2, 0.1, 1.0]])
        P=0.1
        
        x=cp.Variable(shape=(n,m),pos=True)
        snr=np.zeros((n,m))
        for i in range(n):
            for j in range(m):        
                sump=0
                for k in range(m):
                    if k!=j:
                        sump=sump+G[i,k]*P
                snr[i,j]=G[i,j]*P/(sump+sigma[i])
                          #(sigma[i]+cp.sum(G[i,k]*P for k in range(m) if j!=k)))
        #print(snr)        
        #print(snr)
        for i in range(n):
            constraints=[cp.max(snr[i,]*x[i,])>=p_min]
            
        constraints+=[
                     x>=0,
                     x<=1 
                     ]
        for i in range(n):
            constraints+=[cp.sum(x[i,])==1]
        
        obj=cp.Maximize((cp.sum(cp.log(cp.multiply(snr,x)))))
        
        
        problem = cp.Problem(obj, constraints)
        print(problem)
        problem.solve(qcp=True)
        print('value:{}',x.value)
    
    def routing_path(self,src,des,request_rate):
        # src=7
        # des=20
        # request_rate=30
        paths=nx.all_simple_paths(self.G, src,des)
        
        listpath=[]
        for path in paths:
            #print('path',path)
            #get_link_of_path(path)
            #print(get_min_bw_of_path(G, path))
            listpath.append(path)
            
        #print('path from',src,'to',des,':',listpath)
        num_paths=len(listpath)
        #access the attribute of a link
        #print('bw',G[0][1]['bw'])
        num_nodes=self.G.number_of_nodes()    
        num_edges=self.G.number_of_edges()
        #create a bandwidth matrix
        bandwidth=np.zeros((num_nodes,num_nodes))
        for i in range(num_nodes):
            for j in range(num_nodes):            
                if self.G.has_edge(i, j):                
                    bandwidth[i,j]=self.G[i][j]['bw']
        #print('bw',bandwidth)
        ###########################3
        r=cp.Variable(num_paths,pos=True)
        constraints=[]
        #check the link capacity of each path
        list_min_bw_paths=[]
        list_delay_paths=[]
        for path in listpath:
            i=0
            list_min_bw_paths.append(self.get_min_bw_of_path(path))
            list_delay_paths.append(self.get_latency_of_path(path))
            constraints+=[r[i]<=list_min_bw_paths[i]]
            i+=1
        #print(len(list_delay_paths),num_paths)
        obj=cp.Minimize(cp.sum(list_delay_paths*r))
        
        constraints+=[cp.sum(r)==request_rate]
        problem = cp.Problem(obj, constraints)
        #print(problem)
        problem.solve(qcp=True)
        #print('value:',r.value)
        i=0
        for path in listpath:        
            if r.value[i]>0.001:
                print(f'{path} rate  {r.value[i]:.3f}.')
            i+=1
        return listpath,r.value




######################################################


