#!/usr/bin/python3.6

import os
import math
import config_executor


def calc_best_count(bestStrategies, strategies):
	r = config_executor.restrictions['global']
	
	countBest = {}

	for strategy in strategies:
		
		countBest[strategy] = {}

		seg = r.segInf
		while(seg <= r.segSup):	
			countBest[strategy][seg] = {}

			length = r.lenInf
			while(length <= r.lenSup):
				countBest[strategy][seg][length] = 0

				length *= 2

			seg *= 2

	for strategy in strategies:
		
		seg = r.segInf
		while(seg <= r.segSup):	

			length = r.lenInf
			while(length <= r.lenSup):

				for bestStrategiesMachine in bestStrategies:
					if(not seg in bestStrategiesMachine):
						continue

					if(not length in bestStrategiesMachine[seg]):
						continue

					if(bestStrategiesMachine[seg][length] == strategy):
						countBest[strategy][seg][length] += 1

				countBest[strategy][seg][length] = int(round(countBest[strategy][seg][length] * 100 / len(bestStrategies)))
				length *= 2

			seg *= 2

	return countBest


def calc_select_best(countBest):
	r = config_executor.restrictions['global']

	selectedBests = {}
	seg=r.segInf #1
	while seg <= r.segSup:
		selectedBests[seg] = {}
		
		length = r.lenInf
		while length <= r.lenSup:
			if(length/seg <= 1):
				selectedBests[seg][length] = 'noTest'
			else:
				bestStrategy = 'noTest'
				bestValue = 0
				
				for strategy in countBest:
					if(seg in countBest[strategy]):
						if(length in countBest[strategy][seg]):
							if(countBest[strategy][seg][length] > bestValue):
								bestValue = countBest[strategy][seg][length]
								bestStrategy = strategy

				selectedBests[seg][length] = bestStrategy
				
			length *= 2
			
		seg *= 2

	return selectedBests


def calc_min_overload(vecMapVector, bestValues, strategies):
	r = config_executor.restrictions['global']

	selectedBests = {}
	seg=r.segInf
	while seg <= r.segSup:
		selectedBests[seg] = {}
		
		length = r.lenInf
		while length <= r.lenSup:
			if(length/seg <= 1):
				selectedBests[seg][length] = 'noTest'
			else:
				minValue = float('inf')
				bestStrategy = 'noTest'

				for s in strategies:
					if(s.startswith('fixpass')):
						continue

					avg = 0.0
					count = 0.0
					for i in range(0, len(vecMapVector)):
						if(not s in vecMapVector[i]):
							continue
						if(not seg in vecMapVector[i][s]):
							continue
						if(not length in vecMapVector[i][s][seg]):
							continue

						if(not seg in bestValues[i]):
							continue
						if(not length in bestValues[i][seg]):
							continue
						
						count += 1.0
						avg += vecMapVector[i][s][seg][length]/bestValues[i][seg][length]
			
					if(count <= 0):
						continue

					avg /= count
					if(avg < minValue):
						minValue = avg
						bestStrategy = s

				selectedBests[seg][length] = bestStrategy
		
			length *= 2
		
		seg *= 2

	return selectedBests


def calc_best_worst(vecMapVector, bestValues, strategies):
	r = config_executor.restrictions['global']

	selectedBests = {}
	seg=r.segInf
	while seg <= r.segSup:
		selectedBests[seg] = {}
		
		length = r.lenInf
		while length <= r.lenSup:
			if(length/seg <= 1):
				selectedBests[seg][length] = 'noTest'
			else:
				minTime = float('inf')
				bestStrategy = 'noTest'

				for s in strategies:
					maxTime = 0.0;

					for i in range(0, len(vecMapVector)):
						if(s.startswith('fixpass')):
							continue
						
						if(not s in vecMapVector[i]):
							continue
						if(not seg in vecMapVector[i][s]):
							continue
						if(not length in vecMapVector[i][s][seg]):
							continue

						if(not seg in bestValues[i]):
							continue
						if(not length in bestValues[i][seg]):
							continue

						curTime = vecMapVector[i][s][seg][length]/bestValues[i][seg][length]

						if(curTime > maxTime):
							maxTime = curTime

					if(maxTime == 0.0):
						continue

					if(maxTime < minTime):
						minTime = maxTime
						bestStrategy = s

				selectedBests[seg][length] = bestStrategy
		
			length *= 2
		
		seg *= 2

	return selectedBests

def calc_the_scurves(vecMapVector, bestValues, strategies):
	scurves = {}
	for strategy in strategies:
		scurves[strategy] = []	

	for strategy in strategies:	
		if(strategy.startswith('fixpass')):
			continue
		for i in range(0, len(vecMapVector)):
			for seg in vecMapVector[i][strategy]:
				for length in vecMapVector[i][strategy][seg]:
					if(seg not in bestValues[i]):
						continue
					if(length not in bestValues[i][seg]):
						continue

					scurves[strategy].append(vecMapVector[i][strategy][seg][length]/bestValues[i][seg][length])
	
		scurves[strategy] = sorted(scurves[strategy])		

	return scurves


def calc_select_scurves(vecMapVector, selectedBests, bestValues, strategies):
	scurves = {}
	for strategy in strategies:
		scurves[strategy] = {}	
		for s in strategies:
			scurves[strategy][s] = []

	for strategy in strategies:
		for seg in selectedBests:
			for length in selectedBests[seg]:
				if(length/seg <= 1):
					continue

				if(selectedBests[seg][length] == strategy):
					for i in range(0, len(vecMapVector)):
						for s in vecMapVector[i]:
							if(s.startswith('fixpass')):
								continue
								
							if(not s in vecMapVector[i]):
								continue
							if(not seg in vecMapVector[i][s]):
								continue
							if(not length in vecMapVector[i][s][seg]):
								continue

							if(not seg in bestValues[i]):
								continue
							if(not length in bestValues[i][seg]):
								continue

							scurves[strategy][s].append(vecMapVector[i][s][seg][length]/bestValues[i][seg][length])


	for strategy in strategies:
		for s in strategies:
			scurves[strategy][s] = sorted(scurves[strategy][s])

	return scurves


def calc_avg_fix_speedup(vecMapVector):
	print("Caculating fix speedup...")

	r = config_executor.restrictions['global']
	results = {}
	results['all'] = {}
	results['fix'] = {}
	results['sort'] = {}

	seg=r.segInf
	while seg <= r.segSup:
		results['all'][seg] = [[],[],[],[]]
		results['fix'][seg] = [[],[],[],[]]
		results['sort'][seg] = [[],[],[],[]]
		
		length = r.lenInf
		while length <= r.lenSup:
			if(length/seg > 1):
				minAll = float('inf')
				avgAll = 0.0
				maxAll = 0.0

				minFix = float('inf')
				avgFix = 0.0
				maxFix = 0.0
				
				minSort = float('inf')
				avgSort = 0.0
				maxSort = 0.0

				count = 0
				for i in range(0, len(vecMapVector)):
					if(seg not in vecMapVector[i]['fixpasscub']):
						continue
					if(seg not in vecMapVector[i]['fixpassthrust']):
						continue
					if(length not in vecMapVector[i]['fixpasscub'][seg]):
						continue
					if(length not in vecMapVector[i]['fixpassthrust'][seg]):
						continue
			
					fixcubAll = vecMapVector[i]['fixcub'][seg][length]
					fixthrustAll = vecMapVector[i]['fixthrust'][seg][length]
					fixcubFix = vecMapVector[i]['fixpasscub'][seg][length]
					fixthrustFix = vecMapVector[i]['fixpassthrust'][seg][length]
					fixcubSort = fixcubAll-fixcubFix
					fixthrustSort = fixthrustAll - fixthrustFix

					curValueAll = fixcubAll / fixthrustAll
					curValueFix = fixcubFix / fixthrustFix
					curValueSort = fixcubSort / fixthrustSort

					count += 1
					avgAll += curValueAll
					avgFix += curValueFix
					avgSort += curValueSort

					if(curValueAll < minAll): minAll = curValueAll
					if(curValueFix < minFix): minFix = curValueFix
					if(curValueSort < minSort): minSort = curValueSort

					if(curValueAll > maxAll): maxAll = curValueAll
					if(curValueFix > maxFix): maxFix = curValueFix
					if(curValueSort > maxSort): maxSort = curValueSort

				avgAll /= count
				avgFix /= count
				avgSort /= count

				results['all'][seg][0].append(str(length))
				results['all'][seg][1].append(minAll)
				results['all'][seg][2].append(maxAll)
				results['all'][seg][3].append(avgAll)

				results['fix'][seg][0].append(str(length))
				results['fix'][seg][1].append(minFix)
				results['fix'][seg][2].append(maxFix)
				results['fix'][seg][3].append(avgFix)
				
				results['sort'][seg][0].append(str(length))
				results['sort'][seg][1].append(minSort)
				results['sort'][seg][2].append(maxSort)
				results['sort'][seg][3].append(avgSort)

			length *= 2
	
		seg *= 2


	return results













	