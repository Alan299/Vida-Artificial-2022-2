from cgitb import text
from os.path import exists, join
from sre_parse import WHITESPACE
from tkinter import RIGHT

from manimlib import  *
 

def collatz(num):
    while num != 1:
        print(num)

        if num % 2 == 0:
            num  = int(num / 2)
        
        else: 
            num = int(3 * num +1)

    else:
        print(num)
        print('Done')


class CollatzGrid(VGroup):
    CONFIG = {
        'ROWS_LIMIT':10000, #limit of rows per visualization
        'COLORS': [PURPLE_B,GREY_B, WHITE,GREY_BROWN, PINK,ORANGE,BLUE,GREEN,YELLOW,RED],
        'square_config':{
            'color':WHITE,
            'side_length':0.5,
            'fill_color': WHITE,
            'fill_opacity': 0.95},
        'NUMBER': 1000,

        }

    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        self.init()
        
    
    
    def init(self):
        self.n_steps = 0 
        self.grid = VGroup()



    def step(self,num:int):
        """
        num: number to process
        make a collatz step
        
        """
        
        if num  == 1:
            return 1

        if num % 2 == 0:
            return num//2 #integer division
        else:
            return 3*num + 1

    def get_square_config(self,color ):
        """
        color: str hexadecimal representation of a color (WHITE, RED,ORANGE )

        """
        new_square_config= self.square_config

        new_square_config['color'] = color 
        new_square_config['fill_color'] = color

        return new_square_config

    def number_to_pixels(self,number):
        """
        number: number
        convert each digit in a number to 
        pixel representation, each digit as a fixed color.
        return a row of colored squares
        """

        row = VGroup()

        digits = [int(x) for x in str(number)]

        for digit in digits:
            square = Square(**self.get_square_config(self.COLORS[digit]))
            row.add(square)
        row.arrange(RIGHT,buff= 0.02,center = False )

        return row 

    def run(self,number:int, save_file = True, visualization= None, scene = None ):
        """
        number: number to process 
        visualization: must be an Scene or None
        """
        sequence = [number]
        number_name = number 
        while number != 1:
            number = self.step(number) 
            sequence.append(number)
        if save_file:
            fname = 'collatz_'+ str(number_name)+'.txt'
            if exists(fname):
                print('File {} already exists'.format(fname))
                print('Overwriting . . . ')
            with open(fname, 'w') as f:
                for x in sequence:
                    f.write(str(x) + '\n')

        
        self.grid = VGroup()

        #grid.to_edge(UP+RIGHT)
        if visualization is not  None:
            for (i, n ) in enumerate(sequence):
                if i >= self.ROWS_LIMIT:
                    break
                squares = self.number_to_pixels(n)
                if i == 0:
                    squares.to_edge(UP+RIGHT)
                else:
                    squares.next_to(self.grid[i-1],DOWN,buff = 0.02 )
                squares.to_edge(LEFT)
                self.grid.add(squares)
                #self.grid.arrange(DOWN, buff = 0.05,center )
                
                self.become(self.grid)
                self.center()

                scene.wait(0.01)
                

        #self.arrange(DOWN, buff = 0 )
    def update_(self):
        #if number is 1 stop
        if self.NUMBER == 1:
            return 
        #if we reach limit of rows stop updating
        if self.ROWS_LIMIT <= self.n_steps :
            return 


        self.NUMBER = self.step(self.NUMBER)
        squares = self.number_to_pixels(self.NUMBER)
        
        squares.next_to(self.grid, DOWN, buff = 0.05)
        squares.to_edge(LEFT)
        
        self.grid.add(squares)
        self.become(self.grid)

        self.n_steps+= 1

        self.center()

class Test(Scene):
    def construct(self):
        for i in [10, 32, 57, 79]:
            self.collatz_visualization(i)
            self.clear()

    

    def collatz_visualization(self,n: int):
        """
        n: number to process collatz visualization
        """
        collatz = CollatzGrid()

        title = Text("Mapeo de colores: 0,1,2, ... , 9").scale(0.6)
        squares =collatz.number_to_pixels('0123456789') 

        title.to_edge(RIGHT + UP)
        squares.next_to(title, DOWN)

        self.play(Write(title))
        self.play(ShowCreation(squares))

        self.add(collatz)

        ### Número a checar
        NUMBER = n

        title_num = Text(r'Número a procesar: '+ str(NUMBER)).scale(0.7)
        title_num.next_to(squares, DOWN)
        self.play(ShowCreation(title_num))

        collatz.run(NUMBER,save_file = True, visualization= True, scene = self)
        self.wait(5)

        collatz.set_height(FRAME_HEIGHT * 0.95)

        self.play(collatz.animate.to_edge(UP+LEFT), run_time = 3)
        
        #Using updater
        #collatz.NUMBER = 1000
        #collatz.init()
        #collatz.add_updater(lambda m,dt: m.update_())
        self.wait(5)


        







            





        













if __name__== "__main__":
    collatz(10)


    




