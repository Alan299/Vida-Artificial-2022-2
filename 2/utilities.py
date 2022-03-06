import numpy as np 

def read_rule(filename):
    """
    filename: str 
        read rule file 
    
    Return a dictionary with rule 
    {list(int):int } 
    example {'000':1, '111':0}
    """
    

    with open(filename, 'r') as f:

        rule_dict = {}

        line =  f.readline()
        
        
        while line:
            line = line.strip().replace('\n','')
           
            print("LINE: ", line)

            if line != '':
                rule = line.split(" ")
                rule_dict[rule[0]] = int(rule[1])
           
            line = f.readline()
        return rule_dict
def rule_index(triplet):
    L, C, R = triplet
    index = 7 - (4*L + 2*C + R)
    return int(index)
            

def get_rule_from_number(n):
    """
    n: int
    """

    assert n in range(0,256), "Number must be in range 0-255, given:{}".format(n)

    bin = np.binary_repr(n,width = 8 )
    rule  = {}
    for i in range(8):
        k = np.binary_repr(i,3)

        index = rule_index(  tuple( int(s) for s in k )  )

        rule[k] = int(bin[index])

        

       


    return rule 

if __name__ == "__main__":
    print(get_rule_from_number(90))

    #print(read_rule("rule90.txt"))









