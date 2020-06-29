#!/usr/bin/python3.6

from typing import NamedTuple

class Restriction(NamedTuple):
	segInf: int
	segSup: int
	lenInf: int
	lenSup: int

restrictions = {}
restrictions['global'] 		= Restriction(segInf=1,segSup=1048576,lenInf=32768,lenSup=134217728)
restrictions['nthrust.exe'] = Restriction(segInf=1,segSup=2048   ,lenInf=32768,lenSup=134217728)

