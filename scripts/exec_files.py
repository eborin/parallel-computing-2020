#!/usr/bin/python3.6

import subprocess
import os
import math
import config_executor

def exec_loop(dirFiles):

	gRestr = config_executor.restrictions['global'] # Restrições globais

	length = gRestr.lenInf
	while length <= gRestr.lenSup:	
		#print(length) #int(math.log(length,2)))
		
		seg = gRestr.segInf
		while seg <= gRestr.segSup:
			#print(seg) #int(math.log(seg,2)))

			if(seg < length):
				exec(dirFiles, seg, length)

			seg *= 2
		length *= 2
		#print("")

def exec(dirFiles, seg, length):
	entries = os.scandir(dirFiles)
	for entry in entries:
		if(entry.is_dir()):
			exec(entry.path, seg, length)

		if(not entry.is_file()):
			continue
		
		if(not entry.name.endswith('.exe')):
			continue

		if(entry.name in config_executor.restrictions):

			r = config_executor.restrictions[entry.name]
			if(seg >= r.segInf and seg <= r.segSup and length >= r.lenInf and length <= r.lenSup):
				print(seg)
				print(length)
				#print('Executing program: ', entry.path)
				subprocess.run([entry.path, entry.path])
		else:
			print(seg)
			print(length)
			#print('Executing program: ', entry.path)
			subprocess.run([entry.path, entry.path])

def main():
	dirFiles = "./src/"
	print('Executing all programs into directory: ', dirFiles, '.')
	exec_loop(dirFiles)

if __name__ == "__main__":
	main()
