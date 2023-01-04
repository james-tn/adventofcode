from typing import List, Dict
import matplotlib.pyplot as plt
import random
import copy
import numpy as np
import queue
from collections import deque

class Elf():
    def __init__(self, x,y):
        self.x = x
        self.y=y
        self.active = True
        self.last_move =""


    def move(self, direction):
        self.active = True
        if direction == 'n':
            self.x -= 1
        elif direction == 's':
            self.x += 1
        elif direction == "w":
            self.y -= 1
        else:
            self.y += 1

    def step(self,adjacent_positions, action_queue):
        values = adjacent_positions.values()
        if  sum(values) ==0:
            self.active = False

            return # no elf in adjancent positions, do nothing

        self.prev_position = (self.x, self.y) #backup


        for next_action in action_queue:
            considered_positions = [adjacent_positions[x] for x in adjacent_positions.keys() if next_action in x]
            if sum(considered_positions) ==0:
                self.move(next_action)
                
                break
        
        
    def reverse(self):
        self.x, self.y = self.prev_position


class Environment:
    def __init__(self, file_path="day23/input.txt"):
        with open(file_path,"r") as file:
            lines = file.readlines()
        raw_data = [line.strip() for line in lines]
        raw_temp =[]
        self.elfs = []
        for line in raw_data:
            temp = []
            for element in line:
                temp.append(element)
            raw_temp.append(temp)

        raw_data = np.array(raw_temp)
        data = np.where(raw_data=="#", 1, 0 )
        data = np.pad(data, 1000, constant_values=0)
        self.data = data
        i=0
        for line in data:
            j =0
            for element in line:
                if element == 1:
                    elf = Elf(i,j) #initialize elf from data
                    self.elfs.append(elf)
                j += 1
            i += 1
        self.time =0
        self.game_status = "active"
        self.initial= True
        self.action_queue = deque(['n', 's','w', 'e']) 

    def update_matrix(self):
        new_data = np.zeros((self.data.shape[0], self.data.shape[1]))
        for elf in self.elfs:
            new_data[elf.x, elf.y] += 1
        self.data = new_data
    def get_adjacent_cells(self, x,y): #given x,y, get adjacent cell
        #north: x-1, y
        n,ne,nw, s, se, sw, w, e = 2, 2, 2, 2,2,2,2,2 
        if x - 1 >=0: 
            n = self.data[x-1, y]
        if x -1 >=0 and y-1 >=0:
            nw = self.data[x-1, y-1]
        if x-1 >=0 and y +1 <= self.data.shape[1]-1:
            ne = self.data[x-1, y+1]
        if x+1 <= self.data.shape[0] -1:
            s = self.data[x+1, y]
        if x+1 <= self.data.shape[0] -1 and y +1 <= self.data.shape[1]-1:
            se = self.data[x+1, y+1]
        if x+1 <= self.data.shape[0] -1 and y -1 >= 0:
            sw = self.data[x+1, y-1]
        if  y -1 >= 0:
            w = self.data[x, y-1]
        if y +1 <= self.data.shape[1]-1:
            e = self.data[x, y+1]
        return {"n":n,"ne":ne,"nw":nw,"s":s, "se":se,"sw":sw,"w":w,"e":e}


    def check_status(self):
        active = False
        for elf in self.elfs:
            if elf.active:
                active = True
                break
        return active
        
    def validate(self):
        data = np.array(self.data)
        return list(np.argwhere(data>1))
    def step(self):
        self.initial= False
        for elf in self.elfs:
            adjacent_positions = self.get_adjacent_cells(elf.x, elf.y)
            elf.step(adjacent_positions, self.action_queue)
        self.update_matrix()
        invalid_cells = self.validate()
        if len(invalid_cells)>0:
            for cell in invalid_cells:
                for elf in self.elfs:
                    if (cell[0], cell[1]) == (elf.x, elf.y):
                        elf.reverse()
            self.update_matrix()

        self.action_queue.rotate(-1)



    def printout(self):
        i=0
        for row in self.data:
            j=0
            print()
            for item in row:
                if item!=0:
                    print("#", end="")
                else:
                    print(".", end="")
                j += 1
            i += 1

    def count_empty_ground_tiles(self):
        x =[]
        y = []
        for elf in self.elfs:
            x.append(elf.x)
            y.append(elf.y)

        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
        min_rectagle = np.zeros((max_x- min_x+1,max_y - min_y+1))
        for elf in self.elfs:
            min_rectagle[elf.x-min_x, elf.y-min_y] = 1
        return sum(min_rectagle.flatten()==0)


    def get_n_rounds(self):
        n =0 
        while self.check_status():
            self.step()
            n += 1
        return n
if __name__=="__main__":
    env = Environment(file_path="day23/input.txt")
    for i in range(10):
        env.step()
    # env.printout()
    print("part 1 answer: ", env.count_empty_ground_tiles())
    env = Environment(file_path="day23/input.txt")
    print("part 2 answer ", env.get_n_rounds())