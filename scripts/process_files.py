#!/usr/bin/python3.6

import sys
import os
import parse_functions

if(len(sys.argv) < 2):
	print("python3.5 process_files <machine>")
	exit()

dirFiles = str(sys.argv[1])
machine = dirFiles.split("/")[1]
print('Reading directories into directory: ', dirFiles, '".')

if(machine.split('-')[0].lower() == "kahuna"):
	machine = machine.split('-')[1].lower()
else:
	machine = machine.split('-')[0].lower()

parse_functions.scan_machine_dirs(dirFiles, machine)
