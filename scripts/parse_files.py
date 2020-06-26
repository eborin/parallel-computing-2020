#!/usr/bin/python3.5

import sys
import os

REPETITIONS=10

dirFiles = str(sys.argv[1])
print('Reading files into directory "', dirFiles, '".')

vecMap = {}
entries = os.scandir(dirFiles)
for entry in entries:
	if(entry.name.startswith('fixpass')):
		continue
	
	if(not entry.is_file()):
		continue
	
	if(entry.name.endswith('.time')):
		print(dirFiles+entry.name)
		f = open(dirFiles+entry.name)

		lines = f.readlines()
		f.close()

		mapFile = {}
		i = 2
		while (i < len(lines)):
			seg = int(lines[i].strip())
			length = int(lines[i+1].strip())
			i = i+2

			s=0.0
			for i in range(i, i+REPETITIONS):
				s+=float(lines[i].strip())
			s = s/REPETITIONS

			if(not seg in mapFile):
				mapFile[seg] = {}

			mapFile[seg][length] = s
			i=i+2

		vecMap[entry.name.split('.')[0]] = mapFile


from best_strategy import create_tex, calc_best_strategy

bestValues = {}
bestStrategies = {}
calc_best_strategy(vecMap, bestValues, bestStrategies)
create_tex(bestStrategies, dirFiles, "Equal")
