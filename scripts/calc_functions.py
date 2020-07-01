#!/usr/bin/python3.6

import os
import math

def calc_best_strategy(vecMap, bestValues):
	print("Caculating best strategies...")
	
	bestStrategies = {}
	for seg in vecMap['bbsegsort']:
		
		bestStrategies[seg] = {}
		bestValues[seg] = {}

		for length in vecMap['bbsegsort'][seg]:

			minValue = vecMap['bbsegsort'][seg][length]
			minChoice = 'bbsegsort'
		
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

	return bestStrategies


def calc_fix_comparation(vecMap):
	print("Caculating fix comparations...")

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


def calc_fix_relation(vecMap):
	print("Caculating fix relations...")

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