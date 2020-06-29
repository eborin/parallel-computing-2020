#!/usr/bin/python3.6

import sys
import os
from functions import scan_machine_dirs

dirFiles = "./times/"
print('Processing all machines into directory: ', dirFiles, '".')

directories = os.scandir(dirFiles)
for machine in directories:
	if(not machine.is_dir()):
		continue

	print('Reading directories into directory: ', machine.path)
	scan_machine_dirs(machine.path, machine.name)