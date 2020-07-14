#!/usr/bin/python3.6

import os
import math
import config_executor

def calc_best_strategy(vecMap, machine):
	print("Caculating best strategies...")
	
	bestStrategies = {}
	bestValues = {}

	if(machine in config_executor.restrictions):
		r = config_executor.restrictions[machine]	
	else:
		r = config_executor.restrictions['global']
	
	seg = r.segInf
	while(seg <= r.segSup):

		bestStrategies[seg] = {}
		bestValues[seg] = {}

		length = r.lenInf
		while(length <= r.lenSup):
			if(length/seg > 1):
				minValue = float("inf") #vecMap['bbsegsort'][seg][length]
				minChoice = '--'
			
				for strategy in vecMap:

					if(strategy.startswith('fixpass')):
						continue

					if(not seg in vecMap[strategy]):
						continue

					if(not length in vecMap[strategy][seg]):
						continue
					
					if(vecMap[strategy][seg][length] < minValue):
						minValue = vecMap[strategy][seg][length]
						minChoice = strategy

				bestValues[seg][length] = minValue
				bestStrategies[seg][length] = minChoice
			length *= 2

		seg *= 2

	return bestStrategies, bestValues


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
					avg = 0.0
					count = 0.0
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
						
						count += 1.0
						avg += vecMapVector[i][s][seg][length]/bestValues[i][seg][length]

					if(count == 0):
						continue
					
					avg /= count
					if(avg < minValue):
						minValue = avg
						bestStrategy = s

				selectedBests[seg][length] = bestStrategy
		
			length *= 2
		
		seg *= 2

	return selectedBests


def calc_better_worst(vecMapVector, bestValues, strategies):
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
	r = config_executor.restrictions['global']

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
	r = config_executor.restrictions['global']

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

def calc_hou_curve(vecMap):
	r = config_executor.restrictions['global']
	strategy = 'bbsegsort'
	houCurve = {}

	length = r.lenInf
	while length <= r.lenSup:
		houCurve[length] = [[],[]]

		seg=r.segInf
		while seg <= r.segSup:
			if(length/seg <= 1):
				break;
			if(not seg in vecMap[strategy]):
				break;
			if(not length in vecMap[strategy][seg]):
				break;

			#if(seg > 8000):
			houCurve[length][0].append(str(seg))
			houCurve[length][1].append(vecMap[strategy][seg][length])
		
			seg *= 2
		
		length *= 2

	return houCurve


def calc_fix_times(vecMap):
	r = config_executor.restrictions['global']
	strategies = ['fixpasscub','fixpassthrust']
	fixCurve = {}

	for strategy in strategies:
		fixCurve[strategy] = {}
		
		for seg in vecMap[strategy]:
			fixCurve[strategy][seg] = [[],[]]

			for length in vecMap[strategy][seg]:
				fixCurve[strategy][seg][0].append(str(length))
				fixCurve[strategy][seg][1].append(vecMap[strategy][seg][length])
		
			seg *= 2
		
		length *= 2

	return fixCurve



def calc_scurves(vecMap, bestValues):

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

	return scurves



def calc_fix_speedup(vecMap):
	print("Caculating fix speedup...")

	strategy = 'fixcub'
	results = {}
	results['all'] = {}
	results['fix'] = {}
	results['sort'] = {}
	for seg in vecMap[strategy]:

		results['all'][seg] = [[],[]]
		results['fix'][seg] = [[],[]]
		results['sort'][seg] = [[],[]]

		for length in vecMap[strategy][seg]:
			fixcubAll = vecMap['fixcub'][seg][length]
			fixthrustAll = vecMap['fixthrust'][seg][length]
			fixcubFix = vecMap['fixpasscub'][seg][length]
			fixthrustFix = vecMap['fixpassthrust'][seg][length]
			fixcubSort = fixcubAll-fixcubFix
			fixthrustSort = fixthrustAll - fixthrustFix

			results['all'][seg][0].append(str(length))
			results['all'][seg][1].append(fixcubAll / fixthrustAll)

			results['fix'][seg][0].append(str(length))
			results['fix'][seg][1].append(fixcubFix / fixthrustFix)
			
			results['sort'][seg][0].append(str(length))
			results['sort'][seg][1].append(fixcubSort / fixthrustSort)

	return results


def calc_fix_steps(vecMap):
	print("Caculating fix steps...")

	strategy = 'fixcub'
	results = {}
	results['fixcub'] = {}
	results['fixthrust'] = {}

	for seg in vecMap[strategy]:

		results['fixcub'][seg] = [[],[]]
		results['fixthrust'][seg] = [[],[]]

		for length in vecMap[strategy][seg]:
			fixcubAll = vecMap['fixcub'][seg][length]
			fixthrustAll = vecMap['fixthrust'][seg][length]
			fixcubFix = vecMap['fixpasscub'][seg][length]
			fixthrustFix = vecMap['fixpassthrust'][seg][length]

			results['fixcub'][seg][0].append(str(length))
			results['fixcub'][seg][1].append(fixcubFix/fixcubAll*100)
			results['fixthrust'][seg][0].append(str(length))
			results['fixthrust'][seg][1].append(fixthrustFix/fixthrustAll*100)

	return results