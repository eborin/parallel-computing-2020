#!/usr/bin/python3.6

import os
import math
import tex_code
import config_generator
import config_executor
import calc_functions
import parse_functions

def create_tex(bestStrategies, texFile, machine, equalOrDiff):
	parse_functions.removing_existing_file(texFile)
	print("Creating text file: " + texFile)
	f = open(texFile, 'w')

	f.write(tex_code.packages)
	f.write(tex_code.commands)

	if(equalOrDiff == "equal"):
		sizeSegments = " with the \\textbf{same size}"
	else:
		sizeSegments = " with \\textbf{different sizes}"

	caption = sizeSegments + " on \\textbf{" + machine + "}."
	
	f.write(tex_code.header_best_strategy(caption, machine, equalOrDiff))
	
	r = config_executor.restrictions['global']
	seg=r.segInf #1
	while seg <= r.segSup:
		length = r.lenInf
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= r.lenSup:
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


def create_tex_best_count(countBest):
	parse_functions.create_output_dir("output/tex-count/")
	
	r = config_executor.restrictions['global']

	for strategy in countBest:
		texCountFile = "output/tex-count/" + strategy + ".tex"
		parse_functions.removing_existing_file(texCountFile)

		print("Creating text file: " + texCountFile)
		f = open(texCountFile, 'w')

		caption = ""
		f.write(tex_code.packages)
		f.write(tex_code.commands)
		f.write(tex_code.header_count_best(strategy))
		
		seg=r.segInf #1
		while seg <= r.segSup:
			length = r.lenInf
			f.write(" & " + str(int(math.log(seg,2))))

			while length <= r.lenSup:
				
				if(seg in countBest[strategy]):
					if(length in countBest[strategy][seg]):
						if(countBest[strategy][seg][length] == 0):
							f.write(" & --")
						else:
							value = countBest[strategy][seg][length]

							if(value >= 80):
								boldValue = 0.6
							else:
								if(value >= 60):
									boldValue = 0.5
								else: 
									if(value >= 40):
										boldValue = 0.4
									else:
										if(value >= 20):
											boldValue = 0.3
										else:
											boldValue = 0.2

							#f.write(" & \\bold"+ strategy + "{" + str(boldValue) + "}{\\ApplyGradient{" + str(value) + "}}")
							f.write(" & \\bold{" + str(boldValue) + "}{\\ApplyGradient{" + str(value) + "}}")
							#f.write(" & \\ApplyGradient{" + str(value) + "}")
				
				length *= 2
			
			seg *= 2
			f.write("\\\\ \n")

		f.write(tex_code.tail)
		f.close()


def create_tex_the_best(selectedBests, outputfile, caption):
	parse_functions.create_output_dir("output/")
	
	texTheBestFile = outputfile
	parse_functions.removing_existing_file(texTheBestFile)

	print("Creating text file: " + texTheBestFile)
	f = open(texTheBestFile, 'w')

	r = config_executor.restrictions['global']

	f.write(tex_code.packages)
	f.write(tex_code.commands)
	f.write(tex_code.header_the_best(caption))
	
	seg=r.segInf #1
	while seg <= r.segSup:
		
		length = r.lenInf
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= r.lenSup:
			
			if(length/seg <= 1):
				f.write(' & \\noTest')
			
			else:
				f.write(' & \\' + selectedBests[seg][length])
				
			length *= 2
			
		seg *= 2
		f.write("\\\\ \n")

	f.write(tex_code.tailTheBest)
	f.close()

def create_tex_all_bests(countBest):
	parse_functions.create_output_dir("output/")
	
	texAllBestsFile = "output/all-bests.tex"
	parse_functions.removing_existing_file(texAllBestsFile)

	print("Creating text file: " + texAllBestsFile)
	f = open(texAllBestsFile, 'w')

	r = config_executor.restrictions['global']

	f.write(tex_code.packages)
	f.write(tex_code.commands)
	f.write(tex_code.header_all_bests())
	
	seg=r.segInf #1
	while seg <= r.segSup:
		
		length = r.lenInf
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= r.lenSup:
			f.write(" &")
			if(length/seg <= 1):
				f.write(" \\noTest")
			else:
				f.write(" \makecell{")
				count = 0
				for strategy in countBest:
					if(seg in countBest[strategy]):
						if(length in countBest[strategy][seg]):
							if(countBest[strategy][seg][length] >= 1):
								f.write(" \\" + strategy + "\\")
								count += 1
								if(count == 2):
									#f.write(" \\\\ ")
									count = 0
				f.write(" }")
			length *= 2
			
		seg *= 2
		f.write("\\\\ \\hhline{|*{2}{~}||*{13}{-}|} \n")

	f.write(tex_code.tailAllBests)
	f.close()


def create_csv(bestStrategies, csvFile, machine, equalOrDiff):
	parse_functions.removing_existing_file(csvFile)
	print("Creating csv file: " + csvFile)
	f = open(csvFile, 'w')

	caption = "Best results for each combination of array length and number of segments considering segments "
	if(equalOrDiff == "equal"):
		sizeSegments = "with the same size"
	else:
		sizeSegments = "with different sizes"

	caption += sizeSegments + " on " + machine + ".\n"
	
	f.write(caption)
	
	r = config_executor.restrictions['global']
	length = r.lenInf
	while length <= r.lenSup:
		f.write(";"+str(int(math.log(length,2))))
		length *= 2
	f.write("\n")

	seg=r.segInf
	while seg <= r.segSup:
		length = r.lenInf
		f.write(str(int(math.log(seg,2))))

		while length <= r.lenSup:
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


def create_scurve(scurves, scurveFile):
	parse_functions.removing_existing_file(scurveFile)
	print("Creating scurve file: " + scurveFile)
	
	import matplotlib.pylab as plt

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 6])

	for strategy in scurves:
		length = len(scurves[strategy])
		marks = int(length/30+1)
		plt.plot(scurves[strategy], config_generator.symbols[strategy], color=config_generator.colors[strategy], markevery=marks, label=config_generator.abbreviations[strategy])

	plt.ylabel('Normalized Times')
	plt.xticks([]) # hide axis x
	plt.legend() # show line names
	
	plt.savefig(scurveFile, format='eps')
	#plt.show()


def generate_multiple_scurves(scurves, outputdir):
	parse_functions.create_output_dir(outputdir)
	for strategy in scurves:
		create_scurve(scurves[strategy], outputdir + strategy + ".eps")


def create_hou_curve(houCurve, houFile):
	parse_functions.removing_existing_file(houFile)
	print("Creating Hou file: " + houFile)
	strategy = 'bbsegsort'

	import matplotlib.pylab as plt

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 5])
	
	for length in houCurve:
		plt.plot(houCurve[length][0], houCurve[length][1], label=str(length))

	#for seg in houCurve:
#		plt.plot(houCurve[seg], config_generator.symbols[strategy], color=config_generator.colors[strategy], label=config_generator.abbreviations[strategy])

	plt.ylabel('Execution Time')
	plt.xlabel('Number of Segments')
	plt.xticks(rotation=30) # rotate
	plt.subplots_adjust(right=0.75) # increment border
	#plt.xticks([]) # hide axis x
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)) # show line names
	
	plt.savefig(houFile, format='eps')
	#plt.show()

def create_fix_times(fixTimes, fixFile):
	parse_functions.removing_existing_file(fixFile)
	print("Creating Fix file: " + fixFile)

	seg = config_generator.fixtimes_seg
	import matplotlib.pylab as plt

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	#ax.set_ylim([0, 5])
	
	for strategy in fixTimes:
		plt.plot(fixTimes[strategy][seg][0], fixTimes[strategy][seg][1], label=str(strategy))

	plt.ylabel('Execution Time')
	plt.xlabel('Array lenght')
	plt.xticks(rotation=30) # rotate
	plt.legend()
	#plt.subplots_adjust(bottom=0.2, right=0.75) # increment border
	#plt.xticks([]) # hide axis x
	#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)) # show line names
	
	plt.savefig(fixFile, format='eps')
	#plt.show()


def create_fix_speedup(results, fixspeedupFile):
	parse_functions.removing_existing_file(fixspeedupFile)
	print("Creating fix speedup file: " + fixspeedupFile)
	import matplotlib.pylab as plt

	seg = config_generator.fixspeedup_seg

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 9])
	
	for entry in results:
		plt.plot(results[entry][seg][0], results[entry][seg][1], config_generator.fixspeedupSymbols[entry], label=config_generator.fixspeedupLabels[entry])

	plt.legend() # show line names
	plt.ylabel('Speedup')
	plt.xlabel('Array Lenght')

	plt.xticks(rotation=30) # rotate
	plt.subplots_adjust(bottom=0.2) # increment border
	
	plt.show()
	plt.savefig(fixspeedupFile, format='eps')


def create_fix_steps(results, fixstepsFile):
	parse_functions.removing_existing_file(fixstepsFile)
	print("Creating fix relation file: " + fixstepsFile)
	import matplotlib.pylab as plt
	import matplotlib.ticker as mtick

	seg = config_generator.fixsteps_seg

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 70])
	ax.yaxis.set_major_formatter(mtick.PercentFormatter())

	for entry in results:
		plt.plot(results[entry][seg][0], results[entry][seg][1], config_generator.fixstepsSymbols[entry], label=config_generator.fixstepsLabels[entry])

	plt.legend() # show line names
	plt.ylabel('Percentage')
	plt.xlabel('Array Lenght')

	plt.xticks(rotation=30) # rotate
	plt.subplots_adjust(bottom=0.2) # increment border
	
	plt.show()	
	plt.savefig(fixstepsFile, format='eps')

