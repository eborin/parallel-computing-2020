#!/usr/bin/python3.6

import sys
import os
import parse_functions

clean = False
if(len(sys.argv) == 2):
	if(sys.argv[1] == "clear"):
		clean = True

dirFiles = "./times/"
print('Processing all machines into directory: ', dirFiles, '".')

directories = os.scandir(dirFiles)
for machine in directories:
	if(not machine.is_dir()):
		continue

	if(machine.name.split('-')[0].lower() == "kahuna"):
		machineName = machine.name.split('-')[1].lower()
	else:
		machineName = machine.name.split('-')[0].lower()

	print('Reading directories into directory: ', machine.path)
	parse_functions.scan_machine_dirs(machine.path, machineName, clean)