import sys
from libmath import *

def run_app(argv):
    ### Run the application with the given arguments

    a = o2() + vec2(1, 0)  # origin dus 0, 0 + 1, 0 = 1, 0
    b = vec2(5, 6)

    print(a.distance(b))  # geeft dan afstand van punt 1,0 tot 5,6

    pass

if __name__ == "__main__":
    run_app(sys.argv)