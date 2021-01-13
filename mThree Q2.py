file = """4
10:15:46
03:59:08
04:00:08
03:59:09"""

import time
import sys

m = int(input())

initial_H = 100

lst = []
time_list = []

for x in range(m):
    n = str(input())
    time_list = lst.append(n)

print(sorted(time_list)[0])

    