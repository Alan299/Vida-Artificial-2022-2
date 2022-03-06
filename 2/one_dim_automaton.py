#import sys 
#sys.path.append('../images')

import numpy as np 
from manimlib import * 

from utilities import read_rule,get_rule_from_number


white_lower = WHITE.lower()

def get_cell_value(object):
    current_value  = int(object.get_color() != white_lower) 

    return current_value

class OneDim(VGroup):
    CONFIG = {
        "square_config":{
            "color": WHITE,
            "side_length": 0.1,
            "fill_color": WHITE,
            "fill_opacity": 0.85,
        }
    }
    def __init__(self,number_rule,n= 5, **kwargs):
        """
        number_rule: int 

        n: int 
            grid side len 
        """
        
        super().__init__(**kwargs)

        self.number_rule = number_rule  

        self.rule = get_rule_from_number(number_rule)
        
        print("n: {} RULE: {} ".format(self.number_rule, self.rule))

        self.n = n 
        self.squares = VGroup()

        for i in range(self.n):
            vg = VGroup()
            for j in range(self.n):
                vg.add(Square(**self.square_config))

            vg.arrange(RIGHT, buff = 0)
            self.squares.add(vg)

        self.squares.arrange(DOWN, buff = 0)

        self.add(*self.squares)

        #Add only one or two alive cells BLACK color ( 0 as a number)

        self[0][(n//2)].set_color(BLACK)
        """if self.n%2 == 1:
            self[0][(n//2)].set_color(BLACK)
        else:
            self[0][(n//2)-1].set_color(BLACK)
            self[0][(n//2)].set_color(BLACK)
        """

        self.row  = 0

   
    def update_color_cell_2(self,i,j):
        """
        Given i,j (cell position)

        Add new generation i,j based on 
        last generation i-1,j
        """

        cell = self[i-1][j]

        l_cell,r_cell = self[i-1][(j-1)%self.n],self[i-1][(j+1)%self.n]

        current_value  =get_cell_value(cell) #WHITE is 0 BLACK is 1

        #left and right values
        lv, rv = get_cell_value(l_cell),get_cell_value(r_cell)

        neighborhood = ''.join((str(lv),str(current_value),str(rv)))
        

        # New generation cell
        new_cell = self[i][j]

        new_value = None 
        # apply rule 
        try:
            new_value  =self.rule[neighborhood]
            
        except KeyError :
            print("key {} not found in rule ".format(neighborhood))

        if new_value  == 0:
            
            new_cell.set_color(WHITE)
        else:
            new_cell.set_color(BLACK)

    def update_color_cell(self,i,j):
        """
        Given i,j (cell position)

        Add new generation i,j based on 
        last generation i-1,j
        """

        cell = self[i-1][j]

        l_cell,r_cell = self[i-1][(j-1)%self.n],self[i-1][(j+1)%self.n]

        current_value  =get_cell_value(cell) #WHITE is 0 BLACK is 1

        #left and right values

        lv, rv =None, None 
        # If we are at the end of row 
        #we consider left or right neighbor as a dead cell (WHITE cell)
        if j == 0:
            lv = 0
        else: 
            lv = get_cell_value(l_cell)
            
        
        if j == (self.n-1):
            rv = 0 
        else:
            rv  = get_cell_value(r_cell)

        neighborhood = ''.join((str(lv),str(current_value),str(rv)))
        

        # New generation cell
        new_cell = self[i][j]

        new_value = None 
        # apply rule 
        try:
            new_value  =self.rule[neighborhood]
            
        except KeyError :
            print("key {} not found in rule ".format(neighborhood))

        if new_value  == 0:
            
            new_cell.set_color(WHITE)
        else:
            new_cell.set_color(BLACK)

        
    def step(self):

        self.row = (self.row+1) % self.n
        #for each cell in a row 
        #update his state using above state
        for j in range(self.n):
            self.update_color_cell(self.row, j)
    


        
    def run(self, scene, save_image = True ):
        for i in range(self.n-1):
            #Generate new generation 
            #next row of cells
            self.step()
            scene.wait(0.2)
        
        image = scene.get_image()

        image.save("ca_rule{}_size_n{}".format(str(self.number_rule), str(self.n)) + ".png",format = "png")

        


    
#https://towardsdatascience.com/simple-but-stunning-animated-cellular-automata-in-python-c912e0c156a9

#https://matplotlib.org/matplotblog/posts/elementary-cellular-automata/

#https://github.com/IlievskiV/Amusive-Blogging-N-Coding/blob/master/Cellular%20Automata/cellular_automata.ipynb


#https://mathworld.wolfram.com/ElementaryCellularAutomaton.html




