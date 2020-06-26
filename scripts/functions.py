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

		if os.path.exists(texFile):
			os.remove(texFile)
			print("Removing text file: " + texFile)

		vecMap = parse_files(d.path)

		bestValues = {}
		bestStrategies = {}
		calc_best_strategy(vecMap, bestValues, bestStrategies)
		create_tex(bestStrategies, texFile)


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
				if(seg in vecMap[strategy]):
					if(length in vecMap[strategy][seg]):
						if(vecMap[strategy][seg][length] < minValue):
							minValue = vecMap[strategy][seg][length]
							minChoice = strategy

			bestValues[seg][length] = minValue
			bestStrategies[seg][length] = minChoice


def create_tex(bestStrategies, texFile):
	print("Creating text file: " + texFile)
	f = open(texFile, 'w')

	f.write(tex_code.packages)
	f.write(tex_code.commands)
	f.write(tex_code.header)

	seg=1
	while seg <= 1048576:
		length = 32768
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= 134217728:
			if(length/seg <= 1):
				f.write(" & \\noTest")
			else:
				f.write(" & \\" + bestStrategies[seg][length])
			length *= 2
		
		seg *= 2
		f.write("\\\\ \n")

	f.write(tex_code.tail)
