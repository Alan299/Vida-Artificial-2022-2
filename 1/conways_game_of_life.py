#import sys 
#sys.path.append('../images')

from tkinter import W
import numpy as np 
from manimlib import * 


class ConwaysBoardBUG(VGroup):
    CONFIG = {
        "square_config":{
            "color": WHITE,
            "side_length": 0.5,
            "fill_color": WHITE,
            "fill_opacity": 0.85,
        }

    }


    def __init__(self,n= 10,**kwargs):
        self.n = n 
        #self.m = m 
        super().__init__(**kwargs)

        #Create random matrix with 0's and 1's
        random_matrix = np.random.rand(self.n, self.n)
        self.matrix = random_matrix > 0.8
        self.matrix = self.matrix.astype(np.float64)

        

        self.squares = [Square(**self.square_config) 
        for _ in range(self.n*self.n) 
        ]

        self.add(*self.squares)

        

        #self.arrange_in_grid(n_rows = self.n,n_cols = self.n, buff = 0)

        self.arrange_in_grid(n_cols = self.n, buff = 0 )

        

        self.steps = 0 

    def get_flat_index(self,i,j, reverse = True):
        """
        i: int
            row
        j: int
            column

        Return index of list given matrix coordinates
        """
        if reverse:
            return i + self.n+j
        return self.n*i + j 

    def update_color_cell(self,i,j):
        flat_index = self.get_flat_index(i,j)
        if self.matrix[i][j] == 0:
            
            self.squares[flat_index].set_color(WHITE)
        else:
            self.squares[flat_index].set_color(BLACK)


        
    def update_state(self):

        self.steps+= 1 

        if (self.steps)%30 != 0:
            return 


        matrix_copy = self.matrix.copy()
        indices = [(0,1),(1,0),(1,1),(-1,-1),(-1,0),(0,-1), (1,-1), (-1,1)]

        
        n = self.n 

        for i in range(n):
            for j in range(n):
                # Compute neighbor sum
                value  = 0
                for t in indices:
                    r,c = t
                    value +=  matrix_copy[(i+r)%n][(j + c) %self.n] 
    
                # Dead cell
                if matrix_copy[i][j] ==0:
                    #Birth of a cell
                    if value == 3:
                        self.matrix[i][j] = 1
                                         

                # Death of a cell
                else:
                    # Cell die if it has >= 4 neighbors
                    # or  die if has 1 or less neighbor
                    if value >= 4 or value <= 1:
                        #overcrowding and isolation 
                        self.matrix[i][j] = 0
                        
                    # Cell survives if has 2 or 3 neighbors

                # Adjust color of cell 
                self.update_color_cell(i,j)

    def run(self):
        self.add_updater(lambda m,dt: self.update_state())

    def stop(self):
        self.remove_updater(self.update_state)











class ConwaysBoard(VGroup):
    CONFIG = {
        "square_config":{
            "color": WHITE,
            "side_length": 0.5,
            "fill_color": WHITE,
            "fill_opacity": 0.85,
        }

    }


    def __init__(self,n= 10,**kwargs):
        
        super().__init__(**kwargs)

        self.n = n 

        #Create random matrix with 0's and 1's
        random_matrix = np.random.rand(self.n, self.n)
        self.matrix = random_matrix > 0.8
        self.matrix = self.matrix.astype(np.float64)



        #self.squares = [Square(**self.square_config) 
        #for _ in range(self.n*self.n) 
        #]

        #self.add(*self.squares)
        #self.arrange_in_grid(n_rows = self.n,n_cols = self.n, buff = 0)

        self.squares = VGroup()

        for i in range(self.n):
            vg = VGroup()
            for j in range(self.n):
                vg.add(Square(**self.square_config))

            vg.arrange(RIGHT, buff = 0)
            self.squares.add(vg)

        self.squares.arrange(DOWN, buff = 0)

        self.add(*self.squares)

        self.steps = 0 

        

        

    def get_flat_index(self,i,j, reverse = True):
        """
        i: int
            row
        j: int
            column

        Return index of list given matrix coordinates
        """
        if reverse:
            return i + self.n+j
        return self.n*i + j 

    def update_color_cell(self,i,j):
        
        if self.matrix[i%self.n][j%self.n] == 0:
            
            self[i%self.n][j%self.n].set_color(WHITE)
        else:
            self[i%self.n][j%self.n].set_color(BLACK)


        
    def update_state(self):

        self.steps+= 1 

        if (self.steps)%30 != 0:
            return 


        matrix_copy = self.matrix.copy()
        indices = [(0,1),(1,0),(1,1),(-1,-1),(-1,0),(0,-1), (1,-1), (-1,1)]

        
        n = self.n 

        for i in range(n):
            for j in range(n):
                # Compute neighbor 
                
                
                value  = 0
                for t in indices:
                    r,c = t
                    value +=  matrix_copy[(i+r)%n][(j + c) %self.n] 
    
                # Dead cell
                if matrix_copy[i][j] ==0:
                    #Birth of a cell
                    if value == 3:
                        self.matrix[i][j] = 1
                                         

                # Death of a cell
                else:
                    # Cell die if it has >= 4 neighbors
                    # or  die if has 1 or less neighbor
                    if value >= 4 or value <= 1:
                        #overcrowding and isolation 
                        self.matrix[i][j] = 0
                        
                    # Cell survives if has 2 or 3 neighbors

                # Adjust color of cell 
                self.update_color_cell(i,j)

    def run(self):
        self.add_updater(lambda m,dt: self.update_state())

    def stop(self):
        self.remove_updater(self.update_state)



class CustomConwaysBoard(ConwaysBoard):
    
    def __init__(self,n,alive_cells, **kwargs):
        """
        n: int 

        alive_cells: list of tuples [(x1,y1),(x2,y1), . . . ] 

        """
        self.n = n 
        #self.m = m 
        super().__init__(n = n,**kwargs)

        #Populate matrix with alive cells
        M = np.zeros((self.n, self.n))
        #Using tuple indexing
        rows,cols = zip(*alive_cells)
        M[rows,cols] = 1.0

        self.matrix = M
        self.matrix  = self.matrix.astype(np.float64)
            
        #Update cells color 
        for point in  alive_cells:
            (i,j) = point 
            self.update_color_cell(i,j)
      


class TestCustomConwaysBoard(Scene):
    def construct(self):
        
        b = CustomConwaysBoard(n = 20,alive_cells= [(5,5),(5,6),(4,5),(4,4),(0,0),(0,1),(0,2),  ])
            
        #b.set_height(FRAME_WIDTH)
        #b.set_width(FRAME_HEIGHT-1)
        b.scale(0.6)

        print(b.matrix)

        #self.play(ShowCreation(b))
        self.add(b)

        self.wait(3)

        b.run()
        self.wait(10)

        

def get_pentominoes():
    """
    Get list of pentominoes in a  3x3 box
    """

    result = []
    names = ["F", "P", "T", "U","V","W","X","Z"]

    #F
    result.append([(1,0),(0,1),(1,1),(2,1),(0,2)])


    # P
    result.append([(0,0),(1,0),(2,0),(0,1),(1,1)])


    #T 
    result.append([(0,0),(0,1),(0,2),(1,1),(2,1)])

    #U 
    result.append([(0,0),(1,0),(1,1),(0,2),(1,2)])

    #V
    result.append([(0,0),(1,0),(2,0),(2,1),(2,2)])

    #W
    result.append([(0,0),(1,0),(1,1),(2,1),(2,2)])


    #X
    result.append([(0,1),(1,0),(1,1),(1,2),(2,1)])

    #Z

    result.append([(0,0),(0,1),(1,1),(2,1),(2,2)])


    M = np.zeros((15,15))

    result_last = []

    print("Pentominoes:")
    for p in result:

        new_points = [(point[0] + 4 , point[1] +4) for point in p ]
        result_last.append(new_points)


        m= M.copy()

        rows, cols = zip(*new_points)
        m[rows,cols] = 1 

        print(m)

        print()
    
    return result_last, names 

class Pentominoes(Scene):

    def construct(self):

        ps, names = get_pentominoes()

        for (p,n) in zip(ps,names):

            text = Text(n).scale(2)
            text.to_edge(UP+LEFT)
            self.play(Write(text))


        
            b = CustomConwaysBoard(n = 20, alive_cells = p )


            b.scale(0.6)

            self.add(b)
            self.wait(3)

            b.run()

            self.wait(10)

            self.remove(b)
            self.clear()


class TestNewConwaysBoard(Scene):

    def construct(self):

        ps, names = get_pentominoes()

        #b = CustomConwaysBoard(n = 20, alive_cells = [(10,10)]) 

        b = ConwaysBoard(n = 20) 

        b.squares.scale(0.6)

        self.add(b)

        s = b[0][0]
        s.set_color(RED)

        s = b[1][7]
        s.set_color(RED)

        self.add(b)
        self.wait(3)




