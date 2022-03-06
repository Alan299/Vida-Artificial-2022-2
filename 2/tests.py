import sys

sys.path.append(".")

from manimlib import *  

from one_dim_automaton import OneDim


def get_fill_color(object):

    color = object.get_style()

    print("color: ", color)

    return color 

class TestGetValue(Scene):


    def construct(self):

        sq = Square().set_color(WHITE)

        print(get_fill_color(sq))
        print(sq.get_color())
        print("WHITE: ", WHITE.lower())

        current_value  = int(sq.get_color() != WHITE.lower()) 
        print("Current value: ", current_value)

        sq.set_color(BLACK)

        current_value  = int(sq.get_color() != WHITE.lower()) 
        print("Current value: ", current_value)


        self.add(sq)


        self.wait(5)



class TestOneDim(Scene):

    def construct(self):
        title = ""
        n = 101

        for N in range(256):
            title = Text("Rule: {:d} \n n: {:d}".format(N, n))
            title.scale(1.2)
            title.to_edge(UP + LEFT)
            title.set_color_by_gradient(BLUE,BLUE_C, BLUE_E, YELLOW)
            self.play(Write(title, run_time = 0.5))



            aut = OneDim(number_rule = N,n = n)
            aut.set_width(FRAME_HEIGHT)
            self.add(aut)
            aut.run(self)

            
            self.clear()





