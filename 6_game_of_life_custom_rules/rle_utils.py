
import numpy as np 
import re 
from re import sub


file_path = "2x12infinitegrowth.rle"


 

def encode(text):
    '''
    Doctest:
        >>> encode('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW')
        '12W1B12W3B24W1B14W'    
    '''
    return sub(r'(.)\1*', lambda m: str(len(m.group(0))) + m.group(1),
               text)
 
def decode(text):
    '''
    Doctest:
        >>> decode('12W1B12W3B24W1B14W')
        'WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW'
    '''
    return sub(r'(\d+)(\D)', lambda m: m.group(2) * int(m.group(1)),
               text)
 


def get_matrix(file_path = file_path):
    #variable assingment 
    regex = r"[-+]?[0-9]+"
    pattern = re.compile(regex)
    n_rows, n_cols = 0,0

    with open(file_path, 'r') as f:
        for line in f:
            #ignore comments
            if not line.startswith("#"):
                if line.startswith("x"):
                    numbers = pattern.findall(line)
                    n_cols = int(numbers[0])
                    n_rows = int(numbers[1])
                    print("n_cols: {}, n_rows: {}".format(n_cols, n_rows))
                    
                else:
                    print("encoded line: ", line )
                    line = line.replace("!", '') 

                    # lines are separated by a $
                    parts = line.split('$')

                    #create matrix
                    matrix = np.zeros((n_rows, n_cols))

                    for i,p  in enumerate(parts): 
                        j = 0     
                        plain_text = decode(p)
                        len_text = len(plain_text)

                        #populate matrix with 
                        # 1 if 'o' 0 if 'b'
                        for j,c in enumerate(plain_text):
                            matrix[i,j] = 0 if c == 'b'  else 1 
    return matrix 




def get_matrix_from_cells(file_path):

    char_to_int  = lambda x: 0 if x == '.' else 1

    list_matrix = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith("!"):
                continue 
            
            line = line.strip().replace("\n"," ")
            row = [ char_to_int(char) for char in line]

            list_matrix.append(row)

    return np.array(list_matrix)

cells_path = "52514m.cells"


if __name__ == "__main__":
    textin="WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW"
    assert decode(encode(textin)) == textin
    print(decode("o2b2ob4obo"))
    print(decode("6ob2o2bo"))
    print("TEST get_matrix_from_cells ")
    matrix = get_matrix_from_cells(cells_path)    

    print(matrix.shape, matrix[3][5])



    print("TEST GET MATRIX")

    print(get_matrix(file_path= file_path ))

    












                            




