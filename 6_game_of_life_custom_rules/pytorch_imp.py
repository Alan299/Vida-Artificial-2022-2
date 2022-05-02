import numpy as np 

import torch as th
import torch.nn as nn

#https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html



print("CUDA is available? ", th.cuda.is_available())
device = th.device("cuda" if th.cuda.is_available() else 'cpu')

def get_padding(inp_dim,s,out_dim, k  ):
    """
    all int:
    inp_dim: input dimension
    s: stride
    out_dim: ouput dimension
        desired dimension to obtain on input after conv
    k: kernel size

    compute padding of zeros 

    """

    padding = ((out_dim - 1)*s + 1 -inp_dim + k -1)//2

    return padding 

def get_convolution(state):
    """
    state: numpy matrix 
    """
    rows,cols = state.shape

    assert rows == cols, "Must hasve same number of cols and rows, given: r: {} c: {}".format(rows,cols)
    weights = th.tensor([[[[1,1,1],
                    [1,0,1],
                    [1,1,1]]]],
                    #requires_grad = False
                    device = device,
                    dtype = th.float32)

    padding = get_padding(inp_dim = rows ,s=1,out_dim= rows, k= 3)

    conv = nn.Conv2d(in_channels = 1,
        out_channels = 1,
        kernel_size = 3,
        stride= (1,1),
        padding = padding,
        padding_mode = 'zeros',
        bias = False)

    conv.weight = nn.Parameter(weights,requires_grad  = False )

    return conv

def apply_rule(state, conv):
    """
    state: numpy matrix (H,W)

    conv: torch.Conv2d

    return:  numpy_matrix
        new_state
    """

    #add two singleton dimensions
    #one for batch another for channels
    state_extra_dims = state[None,:][None,:]

    #print("State extra dims: ", state_extra_dims.shape )
    state_th  =th.from_numpy(state_extra_dims).float().to(device)
    output = conv(state_th)

    #print("state.shape: ", state.shape)
    #print("output: ",output.shape)

    #eliminate singleton dimensions
    state_th = th.squeeze(state_th) 
    output = th.squeeze(output)


    #Rules 
    #if cell is alive 1, then survives if it has 2 or 3 neighbors, else die of overcrowding
    #of cell is dead 0, then get alive if it has exactly 3 neighbors
    next_state = (
        ((state_th == 1) & (output > 1) & (output  < 4))
        | ( (state_th == 0 ) & (output == 3))).type(th.uint8) 


    return next_state.cpu().numpy()

def apply_custom_rule(state, conv, rule_string ):
    """
    state: numpy matrix (H,W)

    conv: torch.Conv2d

    rule_string: string
        a binary rule to operate with a  boolean matrix 

    return:  numpy_matrix
        new_state
    """

    #add two singleton dimensions
    #one for batch another for channels
    state_extra_dims = state[None,:][None,:]

    state_th  =th.from_numpy(state_extra_dims).float().to(device)
    output = conv(state_th)

    #eliminate singleton dimensions
    state_th = th.squeeze(state_th) 
    output = th.squeeze(output)

    next_state = eval(rule_string)
    

    return next_state.cpu().numpy()


def get_rule(rule):
    """
    rule: string
    return a dictionary with keys 
    B: number of surrounding cells to create a new cell
    S: number of surrounding cells to survive

    Example:
        input B3/S23 (Original game of lige)
        output: {B:[3], S:[2,3]}
    """

    rule_dict = {'B':[], 'S':[]}


    parts = rule.split(r'/')

    for digit in parts[0][1:]:
        rule_dict['B'].append(int(digit))

    for digit in parts[1][1:]:
        rule_dict['S'].append(int(digit))

    return  rule_dict

    

def rule_to_string(rule):
    """
    rule: dictionary
        B: number of surrounding cells to create a new cell
        S: number of surrounding cells to survive
    """
    B = ''
    for digit in rule['B']:
        B += "(output == {}) |".format(digit)
    B =B[:-1]

    S = ''
    for digit in rule['S']:
        S += "(output == {}) |".format(digit)
    S= S[:-1]

    rule_str = """(
        #Born rules
        ( (state_th == 1 ) & {})
        |
        #Survive rules
        ((state_th == 0 ) & {}) ).type(th.uint8)""".format(B,S)

    return rule_str



def tests():
    for n in range(5,2049):
        state = np.random.randint(2, size =(n,n))

        conv= get_convolution(state)

        new_state = apply_rule(state, conv )
        print("state.shape", state.shape,'\n',
        #state
        )
        print("new_state.shape: ", new_state.shape,'\n',
        #new_state
        )
        print()
        assert state.shape == new_state.shape,"Shape must be the same before and after applying rule"

def tests_custom_rule():

    rules = [r'B3/S23',r'B6/S16',r'B36/S23']


    for r in rules:
        rule_str = rule_to_string(get_rule(r))

        print("Rule string: ", rule_str)

        for n in range(5,2049):
            state = np.random.randint(2, size =(n,n))
            conv= get_convolution(state)
            new_state = apply_custom_rule(state, conv,rule_str)
            #print("state.shape", state.shape,'\n',
            #state
            #)
            #print("new_state.shape: ", new_state.shape,'\n',
            #new_state
            #)
            #print()
            assert state.shape == new_state.shape,"Shape must be the same before and after applying rule"



if __name__ == "__main__":
    #tests()
    rule_dict = get_rule(r'B3/S23')
    print(rule_dict)
    print( rule_to_string(rule_dict))

    tests_custom_rule()

   




