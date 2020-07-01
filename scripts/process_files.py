#!/usr/bin/python3.6

import sys
import os

if(len(sys.argv) < 2):
	print("python3.5 process_files <machine>")
	exit()

dirFiles = str(sys.argv[1])
machine = dirFiles.split("/")[1]
print('Reading directories into directory: ', dirFiles, '".')


from functions import scan_machine_dirs

scan_machine_dirs(dirFiles, machine)
