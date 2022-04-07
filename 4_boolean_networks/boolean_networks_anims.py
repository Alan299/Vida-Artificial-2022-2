from pdb import main
from manim import *

from BN import  config_inx,read_config,new_values, config_to_text 

#https://docs.manim.community/en/stable/tutorials/configuration.html


#Boolean Network
class BN(VGroup):
    CONFIG  = {}

    def __init__(self, config,**kwargs):
        super().__init__(**kwargs)
        
        self.config = config 

        """
        nodes:      Int. Count of nodes in network
        values:     List. Initial node values
        conn:       Int. Count of connections per node
        conns:      List-of-list. Connections per node
        conn2val:   List. Truth-table function outputs
        """
        self.nodes, self.values, self.conn, self.conns, self.conn2val = read_config(self.config) 

        #print("Initial values: ", self.values)


        # Create Network (Graph)
        self.vertices = list(range(self.nodes))
        self.edges = [ tuple(x) for x in  self.conns ]

        #Nodes have color depending his value 
        #Blue 0 Red 1 
        vertex_config = {}
        for i,value in enumerate(self.values):
            vertex_config[i] =  {"fill_color": RED if value == 1 else BLUE}
            

        #Boolean network
        self.graph = Graph(
            self.vertices, 
            self.edges,
            layout ="circular",
            labels = True ,
            vertex_config = vertex_config,
            edge_config = {}
            )

        self.add(self.graph)

        self.steps = -1


    def construct_graph(self):
        # Create Network (Graph)
       
        vertex_config = {}
        #Nodes have color depending his value 
        #Blue 0 Red 1 
        for i,value in enumerate(self.values):
            vertex_config[i] =  {"fill_color": RED if value == 1 else BLUE}
            

        #Boolean network
        graph = Graph(
            self.vertices, 
            self.edges,
            layout ="circular",
            labels = True ,
            vertex_config = vertex_config,
            edge_config = {}
            )
        return graph 
    def U(self):
        """
        One step of the execution
        """

        self.steps += 1
        #print("self.steps: ", self.steps )

        if not (self.steps % 30 == 0):
            return 
        
        #print values 
        #pval(values, step)    

        #update self.values in place 
        new_values(self.nodes, self.values,self.conn, self.conns,self.conn2val)
        print("Values: ", self.values )

        new_graph = self.construct_graph()
        self.graph.become(new_graph)



    def run(self):
        self.add_updater(
            lambda m, dt: self.U() )
    
    def stop(self):
        self.remove_updater(
            lambda m: self.U())

class BNTest(Scene):
    CONFIG = {
        'config_index':3,}

    def construct(self):

        INDEX = 4
        nodes, values, conn, conns, conn2val = read_config(config_inx[INDEX])
        config_text = config_to_text(nodes, values, conn, conns, conn2val)
        config_text+= "\n Red: 1, Blue: 0"
        
        t = Text( config_text, stroke_color = WHITE)
        t.scale(0.5)
        t.to_edge(UP+LEFT)

        self.play(Create(t))


        bn = BN(config_inx[INDEX]) 
        self.play(Create(bn))
        bn.run()


        self.wait(2)

        #self.wait(duration=1.0, frozen_frame=True)

        self.wait(20)
 




class TestText(Scene):


    def construct(self):

        t = Text("Jijijija").scale(2)

        self.add(t)

        self.wait(3)
