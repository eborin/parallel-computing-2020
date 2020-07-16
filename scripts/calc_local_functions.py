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

			if(seg < 32000):
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