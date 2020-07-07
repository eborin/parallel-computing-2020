#!/usr/bin/python3.6

import os
import math
import tex_code
import config_generator
import config_executor
import calc_functions
import parse_functions

def create_tex(bestStrategies, texFile, machine, equalOrDiff):
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

def create_best_strategies(bestStrategies, bestFile):
	import matplotlib.pylab as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	
	#y = [1, 2, 3, 4, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1]    

	r = config_executor.restrictions['global']

	col_labels = []
	length = r.lenInf
	while length <= r.lenSup:
		col_labels.append(length)
		length *= 2

	#table_vals = [[11, 12, 13], [21, 22, 23], [31, 32, 33]]
	table_vals = []

	row_labels = []	
	seg=r.segInf #1
	while seg <= r.segSup:
		length = r.lenInf
		row_labels.append(str(int(math.log(seg,2))))

		row_values = []
		while length <= r.lenSup:

			if(length/seg <= 1):
				row_values.append("--")
			else:
				if(length in bestStrategies[seg]):
					row_values.append(config_generator.abbreviations[bestStrategies[seg][length]])
				else:
					row_values.append("--")

			length *= 2

		table_vals.append(row_values)
		
		seg *= 2

	print(table_vals)
	print(row_labels)
	print(col_labels)

	axMain = plt.subplot(2,1,1)
	axTable1 = plt.subplot(2,1,2, frameon =False)
	plt.setp(axTable1, xticks=[], yticks=[]) # a way of turning off ticks

	axMain.plot([1,2,3])

	# Draw table
	the_table = axTable1.table(cellText=table_vals,
	                      colWidths=[0.1] * 3,
	                      rowLabels=row_labels,
	                      colLabels=col_labels,
	                      loc='center')
	the_table.auto_set_font_size(False)
	the_table.set_fontsize(24)
	the_table.scale(4, 4)

	# Removing ticks and spines enables you to get the figure only with table
	#axTable1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
	#axTable1.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)
	#for pos in ['right','top','bottom','left']:
	#    axTable1.gca().spines[pos].set_visible(False)
	axTable1.savefig(bestFile, bbox_inches='tight', pad_inches=0.05)


def create_tex_count_best(countBest):
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

							if(value >= 90):
								boldValue = 1.0
							else:
								if(value >= 70):
									boldValue = 0.8
								else: 
									if(value >= 50):
										boldValue = 0.6
									else:
										if(value >= 30):
											boldValue = 0.4
										else:
											if(value >= 10):
												boldValue = 0.2
											else:
												boldValue = 0.1

							f.write(" & \\bold"+ strategy + "{" + str(boldValue) + "}{" + str(value) + "\\%}")
				
				length *= 2
			
			seg *= 2
			f.write("\\\\ \n")

		f.write(tex_code.tail)
		f.close()


def create_tex_the_best(countBest):
	parse_functions.create_output_dir("output/")
	
	texTheBestFile = "output/the-best.tex"
	parse_functions.removing_existing_file(texTheBestFile)

	print("Creating text file: " + texTheBestFile)
	f = open(texTheBestFile, 'w')

	r = config_executor.restrictions['global']

	f.write(tex_code.packages)
	f.write(tex_code.commands)
	f.write(tex_code.header_the_best())
	
	seg=r.segInf #1
	while seg <= r.segSup:
		
		length = r.lenInf
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= r.lenSup:
			
			if(length/seg <= 1):
				f.write(" & \\noTest")
			
			else:
				
				bestStrategy = 'noTest'
				bestValue = 0
				
				for strategy in countBest:
					if(seg in countBest[strategy]):
						if(length in countBest[strategy][seg]):
							if(countBest[strategy][seg][length] > bestValue):
								bestValue = countBest[strategy][seg][length]
								bestStrategy = strategy

				f.write(" & \\" + bestStrategy)
				
			length *= 2
			
		seg *= 2
		f.write("\\\\ \n")

	f.write(tex_code.tailTheBest)
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
	print("Creating scurve file: " + scurveFile)
	import matplotlib.pylab as plt

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([1, 6])

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
	
	for entry in results:
		plt.plot(results[entry][seg][0], results[entry][seg][1], config_generator.fixcompSymbols[entry], label=config_generator.fixcompLabels[entry])

	plt.legend() # show line names
	plt.ylabel('Speedup')
	plt.xlabel('Array Lenght')

	plt.xticks(rotation=30) # rotate
	plt.subplots_adjust(bottom=0.2) # increment border
	
	plt.show()
	plt.savefig(fixcompFile, format='eps')


def create_fixpass_relation(results, fixpassrelFile):
	print("Creating fix relation file: " + fixpassrelFile)
	import matplotlib.pylab as plt
	import matplotlib.ticker as mtick

	seg = config_generator.fixpassrel_seg

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.set_ylim([0, 70])
	ax.yaxis.set_major_formatter(mtick.PercentFormatter())

	for entry in results:
		plt.plot(results[entry][seg][0], results[entry][seg][1], config_generator.fixpassrelSymbols[entry], label=config_generator.fixpassrelLabels[entry])

	plt.legend() # show line names
	plt.ylabel('Percentage')
	plt.xlabel('Array Lenght')

	plt.xticks(rotation=30) # rotate
	plt.subplots_adjust(bottom=0.2) # increment border
	
	plt.show()	
	plt.savefig(fixpassrelFile, format='eps')

