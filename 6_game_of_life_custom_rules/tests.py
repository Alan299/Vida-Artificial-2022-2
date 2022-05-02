import time 
import sys
sys.path.append('./')

from manimlib import *
from conways_game_of_life import *
from rle_utils import  get_matrix, cells_path,get_matrix_from_cells

class Video(Scene):


    def construct(self):
        #R pentomino
        #https://cs.stanford.edu/people/eroberts/courses/soco/projects/2001-02/cellular-automata/walks%20of%20life/patterns2.html
        n = 50
        offset = n//2 - 2
        #(row,colum) as matrix indices
        points = [(3,2),(3,3),(4,1),(4,2),(5,2)]
        points = [(x[0] + offset,x[1] + offset) for x in points ]

        GL = CustomConwaysBoard(n = n, alive_cells= points)
        GL.set_width(FRAME_HEIGHT)

        self.add(GL)
        GL.run()
        self.wait(80)


#rule = 23/3
#12x2 infinite growth
class InfinitePattern1(Scene):

    def construct(self):
        M = get_matrix(file_path)

        print("INIT MATRIX: ",M ,self.__class__.__name__)
        gl = CustomConwaysBoardInitMatrix(101, init_matrix = M)

        gl.set_width(FRAME_HEIGHT)

        self.play(ShowCreation(gl))

        self.wait(5)

        gl.run()

        self.wait(60*10)

        
class InfinitePattern2(Scene):

    def construct(self):
        M = get_matrix_from_cells(cells_path)

        print("INIT MATRIX: ",M ,self.__class__.__name__)
        gl = CustomConwaysBoardInitMatrix(101, init_matrix = M)

        gl.set_width(FRAME_HEIGHT)

        self.play(ShowCreation(gl))

        self.wait(5)

        gl.run()

        self.wait(60*5)



class CustomRuleTest(Scene):
    def construct(self):
        n = 100
        running_time = 30
        t0 = time.time()
        GL =ConwaysBoardCustomRule(n = n,torch = True, rule =r'B36/S23' )
        GL.set_width(FRAME_HEIGHT)
        self.add(GL)
        GL.run()
        self.wait(running_time)

        print("pytorch GPU time: {} with  n:{}".format(time.time()- t0,n ))

       


