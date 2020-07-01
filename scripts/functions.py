#!/usr/bin/python3.6

import os
import math
import tex_code
import config_generator

def scan_machine_dirs(dirFiles, machine):
	directories = os.scandir(dirFiles)
	for d in directories:
		if(not d.is_dir()):
			continue

		print('Reading files into directory: ', d.path, '".')
		vecMap = parse_files(d.path)

		bestValues = {}
		bestStrategies = {}
		calc_best_strategy(vecMap, bestValues, bestStrategies)

		if(machine.split('-')[0].lower() == "kahuna"):
			machine = machine.split('-')[1].lower()
		else:
			machine = machine.split('-')[0].lower()

		files_name = machine + "-" + d.name

		if(config_generator.texGenerator):
			texFile = "tex/" + files_name + ".tex"
			texFile = texFile.replace('//','/')
			if os.path.exists(texFile):
				os.remove(texFile)
				print("Removing tex file: " + texFile)
			
			create_tex(bestStrategies, texFile, machine.split('-')[0].upper(), d.name)

		if(config_generator.csvGenerator): 
			csvFile = "csv/" + files_name + ".csv"
			csvFile = csvFile.replace('//','/')
			if os.path.exists(csvFile):
				os.remove(csvFile)
				print("Removing csv file: " + csvFile)
			
			create_csv(bestStrategies, csvFile, machine.split('-')[0].upper(), d.name)

		if(config_generator.scurveGenerator): 
			scurveFile = "eps/" + files_name + ".eps"
			scurveFile = scurveFile.replace('//','/')
			if os.path.exists(scurveFile):
				os.remove(scurveFile)
				print("Removing scurve file: " + scurveFile)
			
			create_scurve(vecMap, bestValues, scurveFile)


def parse_files(dirFiles):
	vecMap = {}
	entries = os.scandir(dirFiles)
	for entry in entries:
		if(entry.name.startswith('fixpass')):
			continue
		
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

def calc_best_strategy(vecMap, bestValues, bestStrategies):
	print("Caculating best strategies...")

	for seg in vecMap['bbsegsort']:
		
		bestStrategies[seg] = {}
		bestValues[seg] = {}

		for length in vecMap['bbsegsort'][seg]:

			minValue = vecMap['bbsegsort'][seg][length]
			minChoice = 'bbsegsort'
		
			for strategy in vecMap:
				if(not seg in vecMap[strategy]):
					continue

				if(not length in vecMap[strategy][seg]):
					continue
				
				if(vecMap[strategy][seg][length] < minValue):
					minValue = vecMap[strategy][seg][length]
					minChoice = strategy

			bestValues[seg][length] = minValue
			bestStrategies[seg][length] = minChoice


def create_tex(bestStrategies, texFile, machine, equalOrDiff):
	print("Creating text file: " + texFile)
	f = open(texFile, 'w')

	f.write(tex_code.packages)
	f.write(tex_code.commands)

	if(equalOrDiff == "equal"):
		sizeSegments = "\\\\ with the \\textbf{same size}"
	else:
		sizeSegments = "\\\\ with \\textbf{different sizes}"

	caption = sizeSegments + " on \\textbf{" + machine + "}."
	
	f.write(tex_code.header(caption, machine, equalOrDiff))
	
	seg=1
	while seg <= 1048576:
		length = 32768
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= 134217728:
			if(length/seg <= 1):
				f.write(" & \\noTest")
			else:
				if(length in bestStrategies[seg]):
					f.write(" & \\" + bestStrategies[seg][length])
				else:
					f.write(" & \\noTest")
			length *= 2
		
		seg *= 2
		f.write("\\\\ \n")

	f.write(tex_code.tail)
	f.close()


def create_csv(bestStrategies, csvFile, machine, equalOrDiff):
	print("Creating csv file: " + csvFile)
	f = open(csvFile, 'w')

	caption = "Best results for each combination of array length and number of segments considering segments "
	if(equalOrDiff == "equal"):
		sizeSegments = "with the same size"
	else:
		sizeSegments = "with different sizes"

	caption += sizeSegments + " on " + machine + ".\n"
	
	f.write(caption)
	length = 32768
	while length <= 134217728:
		f.write(";"+str(int(math.log(length,2))))
		length *= 2
	f.write("\n")

	seg=1
	while seg <= 1048576:
		length = 32768
		f.write(str(int(math.log(seg,2))))

		while length <= 134217728:
			if(length/seg <= 1):
				f.write(";--")
			else:
				if(length in bestStrategies[seg]):
					f.write(";" + config_generator.abbreviations[bestStrategies[seg][length]])
				else:
					f.write(";--")
			length *= 2
		
		seg *= 2
		f.write("\n")

	f.close()


def create_scurve(vecMap, bestValues, scurveFile):
	print("Creating scurve file: " + scurveFile)
	import matplotlib.pylab as plt

	scurves = {}
	for strategy in vecMap:
		c = []
		for seg in vecMap[strategy]:
			for length in vecMap[strategy][seg]:
				if(length in bestValues[seg]):
					c.append(vecMap[strategy][seg][length]/bestValues[seg][length])

		scurves[strategy] = sorted(c)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([1, 6])
	#ax.set_yscale('log')



	for strategy in scurves:
		plt.plot(scurves[strategy], config_generator.symbols[strategy], color=config_generator.colors[strategy], markevery=5, label=config_generator.abbreviations[strategy])

	plt.ylabel('Normalized Times')
	plt.xticks([]) # hide axis x
	plt.legend() # show line names
	
	plt.savefig(scurveFile, format='eps')
	#plt.show()