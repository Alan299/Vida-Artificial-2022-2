from http.server import executable
import sys

PY_PATH, TXT_PATH, = 'recursion.py','output.txt'

def execute_quine(py_path,txt_path = 'output.txt'):
    """
    py_path: str
        executable file path (.py)

    txt_path:str
        .txt file path 
        where to write output for py_path file
    
    Execute py_path file 
    and writes his output to txt_path file
    
    """

    orig = sys.stdout
    with open(txt_path, "w") as out:

        sys.stdout = out
        try:
            exec(open(py_path).read())
            
        except ValueError:
            print("Error")

        finally: #always executes
            # Change standard output to default 
            sys.stdout  = orig

print("Executed: ")
print(" {} > {}".format(PY_PATH, TXT_PATH))

#Check if PY_PATH is  a quine
#i.e. a program how prints his own source code 
# execute and write output from recursion.py to output.txt
#then check if PY_PATH == TXT_PATH as a string


def check_quine(py_path,txt_path = 'output.txt'):

    """
    py_path: str
        executable file path (.py)

    txt_path:str
        .txt file path 
        where to write output for py_path file
    
    """

    printed_code = ''

    #open file in read mode 'r'
    with open(txt_path, 'r') as f:
        for line in f:
            printed_code+= line.strip()

    #Read source code

    source_code = ''
    #open file in read mode 'r'
    with open(py_path, 'r') as s:
        for line in s:
            #ommit comments
            if not line.startswith("#"):
                source_code+= line.strip()
    print("Souce code and printed code:")
    print(source_code )
    print()
    print(printed_code)


    return source_code == printed_code

execute_quine(PY_PATH, TXT_PATH)

print("It is a quine? = ",check_quine(PY_PATH, TXT_PATH))





