#!/usr/bin/python3.6

import os
import math
import calc_functions
import gen_functions
import config_generator

def scan_machine_dirs(dirFiles, machine):
	vecMapVector = []
	bestStrategiesMachine = []
	bestValuesMachine = []
	directories = os.scandir(dirFiles)
	for d in directories:
		if(not d.is_dir()):
			continue

		files_name = machine + "-" + d.name

		print('Reading files into directory: ', d.path, '".')
		vecMap = parse_strategies(d.path)
		vecMapVector.append(vecMap)

		bestStrategies, bestValues = calc_functions.calc_best_strategy(vecMap, machine)

		if(config_generator.texGenerator):
			texFile = "output/tex/" + files_name + ".tex"
			create_output_dir("output/tex/")
			gen_functions.create_tex(bestStrategies, texFile, machine.upper(), d.name)

		if(config_generator.csvGenerator):
			csvFile = "output/csv/" + files_name + ".csv"
			create_output_dir("output/csv/")
			gen_functions.create_csv(bestStrategies, csvFile, machine.upper(), d.name)

		if(config_generator.scurveGenerator): 
			scurveFile = "output/scurves/" + files_name + ".eps"
			create_output_dir("output/scurves/")
			scurves = calc_functions.calc_scurves(vecMap, bestValues)
			gen_functions.create_scurve(scurves, scurveFile)

		if(config_generator.fixspeedupGenerator): 
			fixspeedupFile = "output/fix/speedup" + files_name + ".eps"
			create_output_dir("output/fix/speedup")
			results = calc_functions.calc_fix_speedup(vecMap)	
			gen_functions.create_fix_speedup(results, fixspeedupFile)

		if(config_generator.fixstepsGenerator): 
			fixstepsFile = "output/fix/steps/" + files_name + ".eps"
			create_output_dir("output/fix/steps")
			results = calc_functions.calc_fix_steps(vecMap)	
			gen_functions.create_fix_steps(results, fixstepsFile)

		if(config_generator.fixtimesGenerator): 
			fixtimesFile = "output/fix/times/" + files_name + ".eps"
			create_output_dir("output/fix/times/")
			fixtimes = calc_functions.calc_fix_times(vecMap)	
			gen_functions.create_fix_times(fixtimes, fixtimesFile)

		if(config_generator.houGenerator): 
			houFile = "output/hou/" + files_name + ".eps"
			create_output_dir("output/hou/")
			houCurve = calc_functions.calc_hou_curve(vecMap)	
			gen_functions.create_hou_curve(houCurve, houFile)

		bestStrategiesMachine.append(bestStrategies)
		bestValuesMachine.append(bestValues)

	strategies = []
	for strategy in vecMap:
		if(strategy.startswith('fixpass')):
			continue
		strategies.append(strategy)

	return bestStrategiesMachine, bestValuesMachine, strategies, vecMapVector


def delete_output_dir(outputDir):
	import shutil
	if (os.path.exists(outputDir)):
		shutil.rmtree(outputDir)
		print("Deleting output directory: " + outputDir)

def create_output_dir(outputDir):
	if (not os.path.exists(outputDir)):
		os.makedirs(outputDir, exist_ok=True)
		print("Creating output directories: " + outputDir)

def removing_existing_file(filename):
	filename = filename.replace('//','/')
	if os.path.exists(filename):
		os.remove(filename)
		print("Removing file: " + filename)

def parse_strategies(dirFiles):
	vecMap = {}
	entries = os.scandir(dirFiles)
	for entry in entries:
		if(not entry.is_file()):
			continue
		
		if(not entry.name.endswith('.time')):
			continue

		print("Parsing file: " + entry.path)
		f = open(entry.path)

		lines = f.readlines()
		f.close()

		mapFile = {}
		i = 2
		while (i < len(lines)):
			seg = int(lines[i].strip())
			length = int(lines[i+1].strip())
			i = i+2

			if(lines[i].strip() == "--"):
				break

			s=0.0
			count = 0
			while (i < len(lines) and lines[i] != "\n"):
				s += float(lines[i].strip())
				i += 1
				count += 1
				
			s = s/count

			if(not seg in mapFile):
				mapFile[seg] = {}

			mapFile[seg][length] = s
			i += 1

		vecMap[entry.name.split('.')[0]] = mapFile

	return vecMap

