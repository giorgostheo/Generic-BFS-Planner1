
# coding: utf-8

# In[59]:

import sys
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from random import choice
import itertools
from graphviz import Source


# In[60]:


def state2states(state, mode='box'):
    if mode == 'box':
        return state2states_box(state)
    elif mode == 'jugs':
        return state2states_jugs(state)


# In[61]:


def state2states_box(starting_state):
    fn_states = []
    '''
    state is a list of lists,
    the positions that can be filled with boxes that are moved
    '''
    for ind in range(len(starting_state)):
        if not starting_state[ind]:
            continue
#         print([i for i in range(len(starting_state)) if starting_state[i] and i != ind])
        for position in [i for i in range(len(starting_state)) if starting_state[i] and i != ind]:
            state = deepcopy(starting_state)
            element = state[ind].pop()
#             print(position, element)
            state[position].append(element)
            fn_states.append(state)
        state = deepcopy(starting_state)
        if len(state[ind])>1:
            element = state[ind].pop()
            state[choice([i for i in range(len(state)) if not state[i]])].append(element)
            fn_states.append(state)
    
#     print(actionlist)
#     for action in actionlist:
#         states.append(act(action, state))
    
    return fn_states


# In[4]:


def state2states_jugs(state):
    states = []
    Jug1max = 9
    Jug2max = 4
    '''
    1 -> fill 1
    2 -> fill 2
    3 -> fill 1 from 2
    4 -> fill 2 from 1
    5 -> empty 1
    6 -> empty 2
    '''
    actionlist = [1,2,3,4,5,6]
    curr1, curr2 = state
    if curr1 == 0:
        actionlist.pop(actionlist.index(5))
        actionlist.pop(actionlist.index(4))
    if curr2 == 0:
        actionlist.pop(actionlist.index(6))
        actionlist.pop(actionlist.index(3))
    if curr1 == Jug1max:
        actionlist.pop(actionlist.index(1))
        try:
            actionlist.pop(actionlist.index(3))
        except: 
            pass
    if curr2 == Jug2max:
        actionlist.pop(actionlist.index(2))
        try:
            actionlist.pop(actionlist.index(4))
        except: 
            pass
#     print(state)
#     print(actionlist)
    for action in actionlist:
        states.append(act(action, state))
    
    return states


# In[62]:


def act(action, state):
#     print('Start state', state)
#     print('Action', action)
    Jug1max = 9
    Jug2max = 4
    curr1, curr2 = state
    if action == 1:
        curr1 = Jug1max
    if action == 2:
        curr2 = Jug2max   
    if action == 3:
        if curr2+curr1 <= Jug1max:
            curr1 += curr2
            curr2 = 0
        else:
            to_add = Jug1max-curr1
            curr1 = Jug1max
            curr2 = curr2 - to_add
    if action == 4:
        if curr1+curr2 <= Jug2max:
            curr2 += curr1
            curr1 = 0
        else:
            to_add = Jug2max-curr2
            curr2 = Jug2max 
            curr1 = curr1 - to_add
    if action == 5:
        curr1 = 0
    if action == 6:
        curr2 = 0
#     print('End State', (curr1, curr2))


    return (curr1, curr2)


# In[63]:


def prunstates(hist, states, box=True):
    if box:
        for state in states:
            for perm in itertools.permutations(state, len(state)):
                if list(perm) in hist:
#                     print(states)
                    states.pop(states.index(state))
                    break
    else:
        for state in hist:
            if state in states:
                states.pop(states.index(state))
    return states


# In[64]:


def check_end(states, end):
    if not end: return True
    return False


# In[85]:


mode = sys.argv[1]

G = nx.OrderedDiGraph()
if mode == 'box':
    end = [[[1,2,3,4],[],[],[]]]
    states = [[[1,2],[3],[4],[]]]
    G.add_node(tuple(map(tuple,states[0])))
    box = True
else:
    end = [1,2,3,4,5,6,7,8,9]
    states = [(0,0)]
    G.add_node((0,0))
    box=False

hist = []




while 1:
    state = states.pop(0)
    hist.append(state)
    new_states = state2states(state, mode=mode)
    states.extend(new_states)
    states = list(prunstates(hist, states, box=box))
    for nst in states:
        if mode == 'box':
            G.add_node(tuple(map(tuple,nst)))
            G.add_edge(tuple(map(tuple,state)), tuple(map(tuple,nst)))
        else:
            G.add_node(nst)
            G.add_edge(state, nst)

#     print('States produced')
#     print(states()
    if mode == 'box':
        for num in states:
    #         print(num)
    #         input()
            if num in end:
    #             print()
                end.pop(end.index(num))
                print(f'Found box {num}')
    else:
        for num in np.unique(states).tolist():
            if num in end:
                end.pop(end.index(num))
                print(f'Found number {num}')
    if check_end(states, end):
        print('done')
        break
#     input()

path = f'{mode}.dot'
write_dot(G,path)
s = Source.from_file(path)
s.view()

