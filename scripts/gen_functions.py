#!/usr/bin/python3.6

import os
import math
import tex_code
import config_generator
import calc_functions

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
		
		if(strategy.startswith('fixpass')):
			continue

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

def create_fix_comparation(results, fixcompFile):
	print("Creating fix comparation file: " + fixcompFile)
	import matplotlib.pylab as plt

	seg = config_generator.fixcomp_seg

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 9])
	#ax.set_yscale('log')
	
	for entry in results:
		plt.plot(results[entry][seg], config_generator.fixcompSymbols[entry], label=config_generator.fixcompLabels[entry])

	plt.ylabel('Speedup')
	plt.xticks([]) # hide axis x
	plt.legend() # show line names
	
	plt.savefig(fixcompFile, format='eps')
	#plt.show()

def create_fixpass_relation(results, fixpassrelFile):
	print("Creating fix relation file: " + fixpassrelFile)
	import matplotlib.pylab as plt
	import matplotlib.ticker as mtick

	seg = config_generator.fixpassrel_seg

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 70])
	ax.yaxis.set_major_formatter(mtick.PercentFormatter())
	#ax.set_yscale('log')
	
	for entry in results:
		plt.plot(results[entry][seg], config_generator.fixpassrelSymbols[entry], label=config_generator.fixpassrelLabels[entry])

	plt.ylabel('Percentage')
	plt.xticks([]) # hide axis x
	plt.legend() # show line names
	
	plt.savefig(fixpassrelFile, format='eps')
