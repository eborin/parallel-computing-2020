#!/usr/bin/python3.6

import sys
import os
import fileinput

dirFiles = str(sys.argv[1])
for line in fileinput.input(dirFiles, inplace = 1): 
	print(line.replace("Sync kernel error: out of memory\n", ""),end='')

for line in fileinput.input(dirFiles, inplace = 1): 
	print(line.replace("0\n", "--\n"),end='')


