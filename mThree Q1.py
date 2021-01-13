import sys
import math
import re

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# Python 3 chosen language

l, h = [int(i) for i in input().split()]

count = 0

for n in range(l,h):
    x = str(n)
    if '6' in x:
        if '8' in x:
            continue
        count = count+1
    elif '8' in x :
        if '6' in x:
            continue
        count = count+1

print(count)