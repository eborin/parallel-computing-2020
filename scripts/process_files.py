#!/usr/bin/python3.5

import sys
import os

if(len(sys.argv) < 2):
	print("python3.5 process_files <machine>")
	exit()

machine = str(sys.argv[1])
dirFiles = "./times/" + machine
print('Reading directories into directory: ', dirFiles, '".')


from functions import scan_machine_dirs

scan_machine_dirs(dirFiles, machine)
