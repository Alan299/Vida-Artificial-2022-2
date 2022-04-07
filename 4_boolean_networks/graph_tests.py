from manim import *
import manimpango
#https://docs.manim.community/en/stable/tutorials/configuration.html?highlight=CLI#a-list-of-all-cli-flags
#print("All fonts\n",manimpango.list_fonts())

#http://paddy3118.blogspot.com/2020/11/random-boolean-networks-using-python.html

#https://docs.manim.community/en/stable/reference/manim.mobject.graph.Graph.html

class LabeledModifiedGraph(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6, 7, 8]
        edges = [(1, 7), (1, 8), (2, 3), (2, 4), (2, 5),
                 (2, 8), (3, 4), (6, 1), (6, 2),
                 (6, 3), (7, 2), (7, 4)]
        g = Graph(vertices,
            edges,
            layout="circular",
            layout_scale=3,
            labels=True,
            vertex_config={7: {"fill_color": RED}},
                  edge_config={(1, 7): {"stroke_color": RED},
                               (2, 7): {"stroke_color": RED},
                               (4, 7): {"stroke_color": RED}})
        self.play(Create(g))

        print(g.vertices)
        print()
        print(dir(g.vertices[3]))
        print(g.vertices[3].label )

        print( [x if x.startswith("set") else " " for x in   dir(g.vertices[3])  ] )
        self.play(g.vertices[2].animate.set_fill(BLUE))

        self.wait(4)

        #self.play(g)




class LargeTreeGeneration(MovingCameraScene):
    DEPTH = 3#4
    CHILDREN_PER_VERTEX = 3
    LAYOUT_CONFIG = {"vertex_spacing": (0.5, 1)}
    VERTEX_CONF = {"radius": 0.25, "color": BLUE_B, "fill_opacity": 1}

    def expand_vertex(self, g, vertex_id: str, depth: int):
        new_vertices = [f"{vertex_id}/{i}" for i in range(self.CHILDREN_PER_VERTEX)]
        new_edges = [(vertex_id, child_id) for child_id in new_vertices]
        g.add_edges(
            *new_edges,
            vertex_config=self.VERTEX_CONF,
            positions={
                k: g.vertices[vertex_id].get_center() + 0.1 * DOWN for k in new_vertices
            },
        )
        if depth < self.DEPTH:
            for child_id in new_vertices:
                self.expand_vertex(g, child_id, depth + 1)

        return g

    def construct(self):
        g = Graph(["ROOT"], [], vertex_config=self.VERTEX_CONF)
        g = self.expand_vertex(g, "ROOT", 1)
        self.add(g)

        self.play(
            g.animate.change_layout(
                "tree",
                root_vertex="ROOT",
                layout_config=self.LAYOUT_CONFIG,
            )
        )
        self.play(self.camera.auto_zoom(g, margin=1), run_time=0.5)