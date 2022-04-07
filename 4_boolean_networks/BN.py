"""
    Random Boolean Networks - Computerphile
        https://www.youtube.com/watch?v=mCML2B94rUg&ab_channel=Computerphile
    Boolean Dynamics withRandom Couplings:
        https://arxiv.org/pdf/nlin/0204062.pdf?
Created on Fri Nov 13 23:33:15 2020

@author: paddy3118
"""
import random
#from graph_cycles_johnson import Graph


##
## Some example configurations of use
##

config_rnd = """
NODES 7
NODE_VALUES RANDOMISED
CONNEXTIONS 3 RANDOMISED
CONN_TO_VALUE RANDOMISED
"""

config_inx = ["""
NODES 10
NODE_VALUES LIST
  1 1 1 1 1 0 1 1 0 0
CONNEXTIONS 2 TABLE
  0 2
  2 0
  2 1
  3 2
  9 9
  6 9
  1 4
  7 0
  3 8
  8 6
CONN_TO_VALUE LIST
  1 0 1 0
""",
"""
NODES 10    # loop 1 .. 128
NODE_VALUES LIST
  1 1 0 1 1 1 1 1 1 1
CONNEXTIONS 2 TABLE
  0 7
  6 7
  8 0
  6 9
  4 0
  8 9
  6 5
  9 2
  4 7
  5 1
CONN_TO_VALUE LIST
  0 1 1 0
""",
"""
NODES 10    # loop 1..63
NODE_VALUES LIST
  0 0 0 1 1 1 1 0 0 0
CONNEXTIONS 2 TABLE
  6 9
  9 8
  0 0
  6 5
  3 4
  1 3
  8 2
  1 4
  8 3
  0 5
CONN_TO_VALUE LIST
  1 0 0 1
""",
"""
NODES 10     # loops from 1 to 106
NODE_VALUES LIST
  1 1 1 0 1 1 0 0 1 0
CONNEXTIONS 2 TABLE
  4 5
  1 6
  1 7
  9 6
  0 0
  2 1
  2 3
  5 6
  1 3
  6 0
CONN_TO_VALUE LIST
  1 0 0 1
""",
"""
NODES 10    # Loops from 0..127
NODE_VALUES LIST
  0 1 1 0 1 1 0 1 0 1
CONNEXTIONS 2 TABLE
  6 4
  5 3
  2 7
  2 8
  7 9
  3 5
  8 4
  9 7
  1 8
  0 5
CONN_TO_VALUE LIST
  1 0 0 1
""",
"""
NODES 10    # loops 1..218
NODE_VALUES LIST
  1 1 1 0 0 0 1 1 0 0
CONNEXTIONS 2 TABLE
  9 1
  3 7
  5 9
  2 6
  2 1
  2 0
  3 5
  3 4
  8 1
  5 7
CONN_TO_VALUE LIST
  1 0 0 1
""",
"""
NODES 10
NODE_VALUES LIST   # loops 0..381
  0 1 1 1 0 0 1 1 0 1
CONNEXTIONS 2 TABLE
  7 3
  4 0
  3 9
  5 9
  2 3
  1 0
  0 2
  5 0
  6 0
  7 8
CONN_TO_VALUE LIST
  0 1 1 0
""",
"""
NODES 10    # loops 0..511?
NODE_VALUES LIST
  0 1 0 0 0 0 1 0 1 0
CONNEXTIONS 2 TABLE
  7 6
  2 8
  6 5
  7 0
  1 9
  5 2
  0 9
  3 8
  0 1
  7 4
CONN_TO_VALUE LIST
  1 0 0 1
""",
]

##
## End examples
##

def read_config(config):
    """
    Parameter:
        config:     Str. Textual configuration for RBN

    Returns:
        nodes:      Int. Count of nodes in network
        values:     List. Initial node values
        conn:       Int. Count of connections per node
        conns:      List-of-list. Connections per node
        conn2val:   List. Truth-table function outputs
    """

    nodes = values = conn = conns = conn2val = None
    line_gen = (l for l in config.strip().split('\n'))
    for line in line_gen:
        field = line.strip().split()
        record = field[0]
        if record == 'NODES':
            nodes = int(field[1])
        elif record == 'NODE_VALUES':
            if field[1] == 'RANDOMISED':
                values = random.choices([0, 1], k=nodes)
            elif field[1] == 'LIST':
                line = next(line_gen)
                values = [int(f) for f in line.strip().split()]
            else:
                raise ValueError('Cannot Parse NODE_VALUES')
        elif record == 'CONNEXTIONS':
            conn = int(field[1])
            if field[2] == 'RANDOMISED':
                conns = [random.choices(range(nodes), k=conn)
                         for _ in range(nodes)]
            elif field[2] == 'TABLE':
                conns = [[int(x) for x in line.strip().split()]
                         for num, line in zip(range(nodes), line_gen)]
            else:
                raise ValueError('Cannot Parse CONNEXTIONS')
        elif record == 'CONN_TO_VALUE':
            if field[1] == 'RANDOMISED':
                conn2val = random.choices([0, 1], k=2**conn)
            elif field[1] == 'LIST':
                line = next(line_gen)
                conn2val = [int(f) for f in line.strip().split()]
            else:
                raise ValueError('Cannot Parse CONN_TO_VALUE')
    return nodes, values, conn, conns, conn2val


def new_values(nodes, values, conn, conns, conn2val):
    "New from old values and RBN description"
    # Boolean conversion
    connected_vals = [sum(2**x * values[c]
                          for x, c in enumerate(conns[n][::-1]))
                      for n in range(nodes)]
    new_v = [conn2val[cv] for cv in connected_vals]
    values[:] = new_v  # in place overwrite
    return new_v

def config_to_text(nodes, values, conn, conns, conn2val):
    "Convert internal RBN to textual form"
    txt = []
    txt.append(f"NODES {nodes}")
    txt.append( "NODE_VALUES LIST")
    txt.append('  ' + ' '.join(str(v) for v in values))
    txt.append(f"CONNEXTIONS {conn} TABLE")
    for c in conns:
        txt.append('  ' + ' '.join(str(cc) for cc in c))
    txt.append( "CONN_TO_VALUE LIST")
    txt.append('  ' + ' '.join(str(v) for v in conn2val))

    return '\n'.join(txt)

def pval(v, step=None):
    "print node values in order. 0 for 0, space for 1, for visibility"
    line = ''.join(' ' if bit else '0' for bit in v)
    print(f"{(step if step is not None else ''):>4}:  {line}")


def run_example(config , steps =100 ):
    """
    config: string
        configuration for initial state
    steps: int
        number of steps to execute
    """
    nodes, values,conn, conns, conn2val = read_config(config)

    start = nodes,values.copy(),conn,conns,conn2val

    print("Configuration \n \n" + config_to_text(*start))

    print("Runnig:\n")


    config_to_text(nodes, values, conn, conns, conn2val)

    for step in range(steps):
        pval(values, step)
        new_values( nodes, values,conn, conns, conn2val)

    print()
    print("Final values: ",values )

if __name__ == "__main__":
    if False:
        # parsed interesting examples for possible cycle extraction
        examples = [read_config(c) for c in config_inx]
    #run_example(config_rnd, steps = 100 )

    print("CONFIG FILE : ")
    print(  read_config(config_inx[4]), sep= "\n\n"  )


    run_example(config_inx[4], steps = 10 )




    #Read more: from Paddy3118 Go deh!: Random Boolean Networks: (Using Python) http://paddy3118.blogspot.com/2020/11/random-boolean-networks-using-python.html#ixzz7PSxYZs6Q
    #Under Creative Commons License: Attribution Non-Commercial No Derivatives
