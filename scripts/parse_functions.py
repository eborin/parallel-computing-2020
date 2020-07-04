#!/usr/bin/python3.6

import os
import math
import calc_functions
import gen_functions
import config_generator

def scan_machine_dirs(dirFiles, machine):
	directories = os.scandir(dirFiles)
	for d in directories:
		if(not d.is_dir()):
			continue

		files_name = machine + "-" + d.name

		print('Reading files into directory: ', d.path, '".')
		vecMap = parse_strategies(d.path)

		bestValues = {}
		bestStrategies = calc_functions.calc_best_strategy(vecMap, bestValues)

		if(config_generator.texGenerator):
			texFile = "output/tex/tex-" + files_name + ".tex"
			removing_existing_file(texFile)
			create_output_dir("output/tex/")
			gen_functions.create_tex(bestStrategies, texFile, machine.upper(), d.name)

		if(config_generator.csvGenerator):
			csvFile = "output/csv/csv-" + files_name + ".csv"
			removing_existing_file(csvFile)
			create_output_dir("output/csv/")
			gen_functions.create_csv(bestStrategies, csvFile, machine.upper(), d.name)

		if(config_generator.scurveGenerator): 
			scurveFile = "output/scurve/scurve-" + files_name + ".eps"
			removing_existing_file(scurveFile)
			create_output_dir("output/scurve/")
			gen_functions.create_scurve(vecMap, bestValues, scurveFile)

		if(config_generator.fixcompGenerator): 
			fixcompFile = "output/fix/fix-" + files_name + ".eps"
			removing_existing_file(fixcompFile)		
			create_output_dir("output/fix/")
			results = calc_functions.calc_fix_comparation(vecMap)	
			gen_functions.create_fix_comparation(results, fixcompFile)

		if(config_generator.fixpassrelGenerator): 
			fixpassrelFile = "output/fixpass/fixpass-" + files_name + ".eps"
			removing_existing_file(fixpassrelFile)
			create_output_dir("output/fixpass/")
			results = calc_functions.calc_fix_relation(vecMap)	
			gen_functions.create_fixpass_relation(results, fixpassrelFile)


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

