import sys
from random import choice

if __name__ == "__main__":
    n = 100000
    burst = 10
    arrival = n * burst
    priority = 10
    for arg in sys.argv:
        if '-n' in arg:
            n = int(arg.split('=')[1])
        if '-b' in arg:
            burst = int(arg.split('=')[1])
        if '-p' in arg:
            priority = int(arg.split('=')[1])
        if '-t' in arg:
            arrival = int(arg.split('=')[1])
    for i in range(n):
        ti = choice(range(0, arrival + 1))
        bi = choice(range(1, burst + 1))
        pi = choice(range(1, priority + 1))
        print(f'P{i} {ti} {bi} {pi}')
