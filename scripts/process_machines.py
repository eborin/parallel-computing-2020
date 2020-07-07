#!/usr/bin/python3.6

import sys
import os
import parse_functions
import calc_functions
import gen_functions


if(len(sys.argv) == 2):
	if(sys.argv[1] == "clear"):
		parse_functions.delete_output_dir("output")
else:
	dirFiles = "./times/"
	print('Processing all machines into directory: ', dirFiles, '".')

	bestStrategies = []
	directories = os.scandir(dirFiles)
	for machine in directories:
		if(not machine.is_dir()):
			continue

		if(machine.name.split('-')[0].lower() == "kahuna"):
			machineName = machine.name.split('-')[1].lower()
		else:
			machineName = machine.name.split('-')[0].lower()

		print('Reading directories into directory: ', machine.path)
		bestStrategiesMachine, strategies = parse_functions.scan_machine_dirs(machine.path, machineName)
		for best in bestStrategiesMachine:
			bestStrategies.append(best)
		
	countBest = calc_functions.calc_count_best(bestStrategies, strategies)
	gen_functions.create_tex_count_best(countBest)
	gen_functions.create_tex_the_best(countBest)


		