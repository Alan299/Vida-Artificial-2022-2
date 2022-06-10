import numpy as np
from manimlib import *

class BLine(VGroup):
    CONFIG = {
        
        # 'opacity_func': lambda t: 1.1 - t ** 0.24 if t < 0.1 else 1 - 0.95 * t ** 0.18 - 0.05 * t ** 0.05,
        # 'opacity_func': lambda t: 1000 * (1 - t ** 0.00012) if t < 0.1 else 0.75 * (1 - t ** 0.21),
        # 'opacity_func': lambda t: 1250 * (1 - abs(t-0.006) ** 0.0001) if t < 0.12 else 0.72 * (1 - t ** 0.2),
        'opacity_func': lambda t: 1500 * (1 - abs(t-0.009) ** 0.0001),
        'radius': 0.05,
        'layer_num': 10,
        #'rate_func': smooth,
        'rate_func': lambda t: t ** 2,
    }
    def __init__(self,start,end,color, **kwargs):

        VGroup.__init__(self,**kwargs)

        self.color_list = color_gradient([color, WHITE], self.layer_num)
        
        self.line = Line(start, end, color = average_color(color, WHITE),plot_depth=4, **kwargs)
        #self.add(self.line)
    
       
        #self.add(Dot(color=average_color(self.colors[0], WHITE), plot_depth=4).set_height(0.015 * self.radius))
        for i in range(self.layer_num):
            # self.add(Arc(radius= self.radius/self.layer_num * (0.5 + i), angle=TAU, color=self.color_list[i],
            #              stroke_width=100 * self.radius/self.layer_num,
            #              stroke_opacity=self.opacity_func(i/self.layer_num), plot_depth=5))
            arc = Arc(radius= self.radius * self.rate_func((0.5 + i)/self.layer_num),
                angle=TAU,
                color=self.color_list[i],
                stroke_width=101 * (self.rate_func((i + 1)/self.layer_num) - self.rate_func(i/self.layer_num)) * self.radius,
                stroke_opacity=self.opacity_func(self.rate_func(i/self.layer_num)), plot_depth=5)
            arc.move_to(self.line.end)
            self.add(arc)

        self.add(self.line)

class TestBLine(Scene):

    def construct(self):
        bl = BLine(LEFT, RIGHT, BLUE)

        self.play(ShowCreation(bl))

        self.wait(5)




class Lsystem(VGroup):
    CONFIG = {
        'rules': {'F': 'F+F--F+F'},
        'length': 1,
        'start_loc': ORIGIN,
        'angle': PI / 3,
        'start_rot': 0,
        'iteration': 1,
        'initial': 'F',
        'actions': {},
        'locations': [],
        'rotations': [],
        'graphs': [],
        'expression': '',
        'animation': None,
        'weight': 1,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)

        super().__init__(**kwargs)
        self.kwargs = kwargs
        self.setup()
        self.tree = VGroup()
        self.generate()
        self.draw()


        #VGroup.__init__(self, *self.tree)

    def setup(self):
        #number of steps  taken
        self.step_count = 0

        #iteration count
        self.iteration_count = 0 

        self.exp_count = 0 


        self.actions['F'] = self.draw_forward
        self.actions['+'] = self.rotate_forward
        self.actions['-'] = self.rotate_backward
        self.actions['['] = self.push
        self.actions[']'] = self.pop
        self.cur_loc = self.start_loc
        self.cur_rot = self.start_rot
        self.expression = self.initial

    def draw_forward(self):

        #location and rotation
        o = self.cur_loc
        l = self.length
        a = self.cur_rot

        #new position
        #current location + length and rotation
        e = (o + 
            l * np.cos(a) * RIGHT + 
            l * np.sin(a) * UP)
        #new location
        self.cur_loc = e
        #create line with origin o, destination e
        g = BLine(o, e,**self.kwargs)

        self.tree.add(g)
        self.add(g)

    def rotate_forward(self):
        self.cur_rot += self.angle

    def rotate_backward(self):
        self.cur_rot -= self.angle

    def push(self):
        self.locations.append(self.cur_loc)
        self.rotations.append(self.cur_rot)

    def pop(self):
        self.cur_loc = self.locations.pop()
        self.cur_rot = self.rotations.pop()

    def generate(self):
        for i in range(self.iteration):
            #print(f'generating iteration {i + 1}')
            new_exp = ''
            for e in self.expression:
                new_exp += self.rules.get(e, e)
            self.expression = new_exp
            #print(f'iteration {i + 1} is finished')

    def draw(self):
        count = self.expression.count("F")
        #print(f'Total {count} Fs')
        for e in self.expression:
            act = self.actions.get(e, None)
            if act is not None:
                act()

    def step(self):

        if self.step_count % 10 != 0:
            return 

        action = self.actions.get(self.expression[self.exp_count])


        #increment exp_count
        self.exp_count= (self.exp_count + 1) % (len(self.expression))

        

class Test(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        #points = [np.sin(-10+t/10)*UP/2+DOWN*3+(-10+t/10)*RIGHT for t in range(200)]
        #soil = Polygon(5*DOWN+10*LEFT, *points, 5*DOWN+10*RIGHT, fill_opacity=1, fill_color='#363B25', stroke_width=0)
        #self.add(soil)

        tree1 = Lsystem(
            iteration=5, start_loc=[-7, -3.5, 0], angle=25.7 * DEGREES, color='#5B622E', stroke_width=1,
            rules={'F': 'F[+F]F[-F]F'}, initial='F', length=0.03, start_rot=75 * DEGREES,
        )
        tree2 = Lsystem(
            iteration=5, start_loc=[-4, -3.5, 0], angle=20 * DEGREES, color='#F6C555', stroke_width=1,
            rules={'F': 'F[+F]F[-F][F]'}, initial='F', length=0.12, start_rot=90 * DEGREES,
        )
        tree3 = Lsystem(
            iteration=4, start_loc=[-3, -3.5, 0], angle=22.5 * DEGREES, color='#855B32', stroke_width=1,
            rules={'F': 'FF-[-F+F+F]+[+F-F-F]'}, initial='F', length=0.12, start_rot=75 * DEGREES,
        )
        tree4 = Lsystem(
            iteration=7, start_loc=[0, -3.5, 0], angle=20 * DEGREES, color='#E98B2A', stroke_width=1,
            rules={'X': 'F[+X]F[-X]+X', 'F': 'FF'}, initial='X', length=0.02, start_rot=60 * DEGREES,
        )
        tree5 = Lsystem(
            iteration=7, start_loc=[3, -3.5, 0], angle=25.7 * DEGREES, color='#86C166', stroke_width=1,
            rules={'X': 'F[+X][-X]FX', 'F': 'FF'}, initial='X', length=0.03, start_rot=90 * DEGREES,
        )
        tree6 = Lsystem(
            iteration=6, start_loc=[7, -3.5, 0], angle=22.5 * DEGREES, color='#FEDFE1', stroke_width=1,
            rules={'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}, initial='X', length=0.05, start_rot=110 * DEGREES,
        )

        #self.add(tree1, tree2, tree3, tree4, tree5, tree6)

        #self.wait(5)
        #turn_animation_into_updater(GrowFromRandom(tree1, run_time=4))

        
        trees = [tree1, tree2, tree3, tree4, tree5, tree6]
        for tree in trees:
            self.play(
                ShowCreation(tree), run_time=12, rate_func=linear,
            )
            self.wait()
        '''
        self.wait(5)
        self.play(FadeOutFromRandom(VGroup(*self.mobjects[1:])))
        self.wait()
        '''


class T1(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        tree = Lsystem(
            iteration=7, start_loc=[0, -3.5, 0], angle=25.7 * DEGREES, color=YELLOW, stroke_width=1,
            rules={'X': 'F[+X][-X]FX', 'F': 'FF'}, initial='X', length=0.03, start_rot=90 * DEGREES,
        )

     
        self.play(
            ShowCreation(tree), run_time=10, rate_func=linear,
         )
        self.wait(3)
    


class T2(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        tree = Lsystem(
            iteration=6, start_loc=[0, -3.5, 0], angle=22.5 * DEGREES, color='#FEDFE1', stroke_width=1,
            rules={'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}, initial='X', length=0.05, start_rot=110 * DEGREES,
        )

    
        self.play(
                ShowCreation(tree), run_time=10, rate_func=linear,
            )

        self.wait(3)



class T3(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        tree = Lsystem(
        iteration=5, start_loc=[0, -3.5, 0], angle=22.5 * DEGREES, color='#855B32', stroke_width=1,
        rules={'F': 'FF-[-F+F+F]+[+F-F-F]'}, initial='F', length=0.12, start_rot=75 * DEGREES,
        )
    

    
        self.play(
                ShowCreation(tree), run_time=10, rate_func=linear,
            )

        self.wait(3)

class T4(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        tree =  Lsystem(
        iteration=7, start_loc=[0, -3.5, 0], angle=20 * DEGREES, color='#E98B2A', stroke_width=1,
        rules={'X': 'F[+X]F[-X]+X', 'F': 'FF'}, initial='X', length=0.02, start_rot=60 * DEGREES,
            )
    

    
        self.play(
                ShowCreation(tree), run_time=10, rate_func=linear,
            )

        self.wait(3)



class T5(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        tree =   Lsystem(
        iteration=7, start_loc=[3, -3.5, 0], angle=25.7 * DEGREES, color='#86C166', stroke_width=1,
        rules={'X': 'F[+X][-X]FX', 'F': 'FF'}, initial='X', length=0.03, start_rot=90 * DEGREES,
        )
    
        self.play(
                ShowCreation(tree), run_time=10, rate_func=linear,
            )

        self.wait(3)


class T6(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": '#58B2DC',
            },
        }
    def construct(self):

        """points = [np.sin(-10+t/10)*UP/2+DOWN*3+(-10+t/10)*RIGHT for t in range(200)]
        soil = Polygon(5*DOWN+10*LEFT, *points, 5*DOWN+10*RIGHT, fill_opacity=1, fill_color='#363B25', stroke_width=0)
        self.add(soil)
        """

    
    
        tree = Lsystem(
        iteration=6, start_loc=[7, -3.5, 0], angle=22.5 * DEGREES, color='#FEDFE1', stroke_width=1,
        rules={'X': 'F-[[X]+X]+F[+FX]-X', 'F': 'FF'}, initial='X', length=0.05, start_rot=110 * DEGREES,
        )

    
        self.play(
                ShowCreation(tree), run_time=10, rate_func=linear,
            )

        self.wait(3)