import os
import math
import tex_code

def scan_machine_dirs(dirFiles, machine):
	directories = os.scandir(dirFiles)
	for d in directories:
		if(not d.is_dir()):
			continue

		print('Reading files into directory: ', d.path, '".')
		
		texFile = dirFiles + '/' + machine + "-" + "Best-" + d.name + ".tex"
		csvFile = dirFiles + '/' + machine + "-" + "Best-" + d.name + ".csv"

		if os.path.exists(texFile):
			os.remove(texFile)
			print("Removing text file: " + texFile)

		if os.path.exists(texFile):
			os.remove(csvFile)
			print("Removing text file: " + csvFile)

		vecMap = parse_files(d.path)

		bestValues = {}
		bestStrategies = {}
		calc_best_strategy(vecMap, bestValues, bestStrategies)
		create_tex(bestStrategies, texFile, machine.split('-')[0].upper(), d.name)
		create_csv(bestStrategies, csvFile, machine.split('-')[0].upper(), d.name)


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
		sizeSegments = "with the \\textbf{same size}"
	else:
		sizeSegments = "with \\textbf{different sizes}"

	caption = sizeSegments + " on \\textbf{" + machine + "}."
	
	f.write(tex_code.header(caption))
	
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
	
	seg=1
	while seg <= 1048576:
		length = 32768
		f.write(str(int(math.log(seg,2))))

		while length <= 134217728:
			if(length/seg <= 1):
				f.write(";--")
			else:
				if(length in bestStrategies[seg]):
					f.write(";" + bestStrategies[seg][length])
				else:
					f.write(";--")
			length *= 2
		
		seg *= 2
		f.write("\n")

	f.close()