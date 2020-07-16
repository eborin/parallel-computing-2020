#!/usr/bin/python3.6

import sys
import os
import parse_functions
import calc_global_functions as calc_functions
import gen_functions


if(len(sys.argv) == 2):
	if(sys.argv[1] == "clear"):
		parse_functions.delete_output_dir("output")
else:
	dirFiles = "./times/"
	print('Processing all machines into directory: ', dirFiles, '".')

	bestStrategies = []
	bestValues = []
	vecMaps = []

	directories = os.scandir(dirFiles)
	for machine in directories:
		if(not machine.is_dir()):
			continue

		if(machine.name.split('-')[0].lower() == "kahuna"):
			machineName = machine.name.split('-')[1].lower()
		else:
			machineName = machine.name.split('-')[0].lower()

		print('Reading directories into directory: ', machine.path)
		bestStrategiesMachine, bestValuesMachine, strategies, vecMapsMachine = parse_functions.scan_machine_dirs(machine.path, machineName)
		
		for best in bestStrategiesMachine:
			bestStrategies.append(best)

		for best in bestValuesMachine:
			bestValues.append(best)

		for vecMap in vecMapsMachine:
			vecMaps.append(vecMap)

		
	countBest = calc_functions.calc_best_count(bestStrategies, strategies)
	gen_functions.create_tex_best_count(countBest)
	
	scurves = calc_functions.calc_the_scurves(vecMaps, bestValues, strategies)
	gen_functions.create_scurve(scurves, "output/scurve.eps")

	fixspeedup = calc_functions.calc_avg_fix_speedup(vecMaps)	
	gen_functions.create_avg_fix_speedup(fixspeedup, "output/avg-fix-speedup.eps")
	
	selectedBests = calc_functions.calc_select_best(countBest)
	gen_functions.create_tex_the_best(selectedBests, "output/best-count.tex", "Each scenario with the best strategy in the most of the cases considering all GPUs results")
	scurves = calc_functions.calc_select_scurves(vecMaps, selectedBests, bestValues, strategies)
	gen_functions.generate_multiple_scurves(scurves, "output/scurves/best-count/")

	selectedBests = calc_functions.calc_min_overload(vecMaps, bestValues, strategies)
	gen_functions.create_tex_the_best(selectedBests, "output/min-overload.tex", "Each scenario with the strategy which results in the average less impact between all GPUs results")
	scurves = calc_functions.calc_select_scurves(vecMaps, selectedBests, bestValues, strategies)
	gen_functions.generate_multiple_scurves(scurves, "output/scurves/min-overload/")
	
	selectedBests = calc_functions.calc_best_worst(vecMaps, bestValues, strategies)
	gen_functions.create_tex_the_best(selectedBests, "output/best-worst.tex", "Each scenario with the strategy which results in the best worst time between all GPUs results")
	scurves = calc_functions.calc_select_scurves(vecMaps, selectedBests, bestValues, strategies)
	gen_functions.generate_multiple_scurves(scurves, "output/scurves/best-worst/")
