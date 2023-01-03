import queue

# Breadth First Search #
# visited_set
# parent_map: {node: (parent, actions)}
# Queue q
# starting position
# v = starting position
# q.enqueue(starting_position)
# while q not empty():
# v = q.dequeue()
# if v is the goal then return v
# adjancent_nodes, actions = get_adjancent_nodes(v)
# for each node in adjancent_nodes:
    # if node is not in visited_set:
        #q.enqueue(node)
        # node.parent = v
        # node.parent_actions = actions
        # visited_set.add(node)
from typing import List
import matplotlib.pyplot as plt
import random
import copy
import numpy as np
class Position:
    def __init__(self, x,y):
        self.x = x
        self.y=y
class Elf(Position):
    def step(self,direction:str):
        self.prev = (self.x, self.y)
        if direction =="up":
            self.x += -1
        elif direction =="down":
            self.x += 1
        elif direction =="left":
            self.y += -1
        elif direction =="right":
            self.y += 1
    def backup(self):
        self.x, self.y = self.prev
class Environment:
    def __init__(self, entrance=None,file_path="day24/input.txt", elf =None):
        with open(file_path,"r") as file:
            lines = file.readlines()
        raw_data = [line.strip() for line in lines]
        raw_temp =[]
        for line in raw_data:
            temp = []
            for element in line:
                temp.append(element)
            raw_temp.append(temp)
        raw_data = np.array(raw_temp)
        inner_data = raw_data[1:raw_data.shape[0]-1,1:raw_data.shape[1]-1]
        outer_data = np.where(raw_data=="#", 1, 0 )
        if not elf:
            self.elf = Elf(0, 1)
        else:
            self.elf = Elf(elf[0], elf[1])
        outer_data[self.elf.x,self.elf.y] = 0

        if not entrance:
            self.entrance = outer_data.shape[0]-1,outer_data.shape[1]-2

        else:
            self.entrance = entrance
        outer_data[self.entrance[0],self.entrance[1]] =-1

        self.outer_data = outer_data
        self.left_data = np.where(inner_data=="<", 2, 0 )
        self.right_data = np.where(inner_data==">",4, 0)
        self.up_data = np.where(inner_data=="^",3, 0)
        self.down_data = np.where(inner_data=="v",5, 0)
        self.time =0
        self.game_status = "active"
        self.initial= True
    def check_status(self):
        data = self.get_data()
        if (self.elf.x, self.elf.y) == self.entrance:
            return 1
        if not self.initial and (self.elf.x >= data.shape[0]-1 or self.elf.y >= data.shape[1]-1 or self.elf.x <0 or self.elf.y <0):
            return -1
        value = data[self.elf.x][self.elf.y]

        if value == -1:
            return 1
        elif value ==0:
            return 0
        else: return -1
        
    def get_data(self):
        re_inner_data = self.left_data+self.right_data+self.up_data + self.down_data
        re_inner_data = np.pad(re_inner_data,1,constant_values=0)
        return re_inner_data + self.outer_data
    def progress_env(self, n_steps, reset_state=False):
        # print("progress received n_steps ", n_steps, "reset_state ", reset_state, " time ", self.time )


        if not reset_state:
            self.time += n_steps
            roll_steps = n_steps
        else:
            roll_steps = n_steps- self.time
            self.time = n_steps
        self.left_data =np.roll(self.left_data,-roll_steps,axis =1)
        self.right_data =np.roll(self.right_data,roll_steps,axis =1)
        self.up_data =np.roll(self.up_data,-roll_steps,axis =0)
        self.down_data =np.roll(self.down_data,roll_steps,axis =0)
        # assert self.check_status() >=0, str(self.elf.x) + " " + str(self.elf.y) + " " + str(hash(str(env.get_data()))) + " time " + str(self.time)

    def backup(self):

        self.elf.backup()
        # print("call progress_env at backup")
        self.progress_env(-1)

    def step(self,direction) -> int:
        self.initial= False
        # print("call progress at step")
        self.progress_env(1)
        self.elf.step(direction)
        if self.check_status() <0:
            self.game_status = "over"
            return -1
        elif self.check_status() >0:
            self.game_status = "done"
            return 1
        else: 
            self.game_status = "active"
            return 0
    def printout(self):
        data = self.get_data()
        i=0
        for row in data:
            j=0
            print()
            for item in row:
                if (i,j) == (self.elf.x,self.elf.y):
                    if item!=0:
                        print("X", end="")
                    else:
                        print("E", end="")
                else:
                    if item==1:
                        print('#', end="")
                    elif item==0 or item ==-1:
                        print(".", end="")
                    elif item == 2:
                        print("<", end="")
                    elif item == 4:
                        print(">", end="")
                    elif item == 3:
                        print("^", end="")
                    elif item == 5:
                        print("v", end="")
                    else:
                        print("&", end="")
                j += 1
            i += 1

    def clone(self):
        env = copy.deepcopy(self)
        return env

def test_action(action, env):
        reward = env.step(action)
        status = env.check_status()
        x,y, time = env.elf.x, env.elf.y, env.time
        env_state = hash(str(env.get_data()))
        env.backup()

        return reward >= 0, (x,y,env_state, time)
def get_adjacents(node, env):
    
    output=[]
    ok_actions =[]
    env_hash = hash(str(env.get_data()))
    node_id = (node[0], node[1], env_hash)
    for action in ["wait", "up","down", "left", "right"]:
        result = test_action(action, env)
        if result[0]:
            output.append((result[1][0],result[1][1],result[1][2],result[1][3],[action]))
            ok_actions.append(action)
    waits=[]
    wait_count =0
    env.progress_env(-wait_count) #reverse environment back

    return output
def find_shortest_path(file_path="day24/input.txt",starting_time=0, starting_position=(0,1), entrance = (21,150)):
    dead_nodes = []
    visited_nodes = set()

    q = queue.Queue()


    env = Environment(file_path=file_path,entrance=entrance, elf=starting_position)
    env.progress_env(starting_time,reset_state=True)

    data = env.get_data()


    parent_map = {}
    env_hash = hash(str(env.get_data()))
    starting_node = ((starting_position[0], starting_position[1], env_hash),starting_time)
    q.put(starting_node)
    solutions = []
    while not q.empty():
        node = q.get()
        # print(node)
        if (node[0][0], node[0][1]) == entrance:
            ##handle retrieving
            actions = []
            node_id = (node[0][0], node[0][1], node[0][2])
            while True:
                parent = parent_map.get(node_id,"")
                if parent !="":
                    node_id = parent[0]
                    actions = parent[1] + actions
                    if node_id == (starting_position[0], starting_position[1], env_hash):
                        break
            solutions.append(actions)
        

        
        env.elf.x, env.elf.y = node[0][0],node[0][1] #update elf position for environment
        time = node[1]
        env.progress_env(time,reset_state=True) #update the environment progress
        assert env.check_status() >= 0, "time " + str(time)  + " x, y " + str(env.elf.x) + " " + str(env.elf.y)
        adjacent_items = get_adjacents(node, env)

        for adjacent_item in adjacent_items:
            adjacent_node = (adjacent_item[0], adjacent_item[1],adjacent_item[2])
            if adjacent_node not in visited_nodes:
                visited_nodes.add(adjacent_node)
                q.put((adjacent_node,adjacent_item[3]))
                parent_map[adjacent_node]= (node[0],adjacent_item[4])
    if len(solutions)>0:
        solutions.sort(key = lambda x: len(x))
        # print("actions ", solutions[0])
        print("time ", len(solutions[0]))
        return len(solutions[0])
    else:
        print("solution not found")
if __name__=="__main__":
    stage1 = find_shortest_path(starting_time=0, starting_position=(0,1), entrance = (21,150))
    print("stage 1 takes ",stage1)
    stage2 = find_shortest_path(starting_time=stage1, starting_position=(21,150), entrance = (0,1))
    print("stage 2 takes ",stage2)
    stage3 = find_shortest_path(starting_time=stage1+stage2, starting_position=(0,1), entrance = (21,150))
    print("stage 3 takes ",stage3)
    print("total time for 3 trips ", stage1+stage2+stage3)
