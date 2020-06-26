import math

def calc_best_strategy(vecMap, bestValues, bestStrategies):

	for seg in vecMap['bbsegsort']:
		
		bestStrategies[seg] = {}
		bestValues[seg] = {}

		for length in vecMap['bbsegsort'][seg]:

			minValue = vecMap['bbsegsort'][seg][length]
			minChoice = 'bbsegsort'
		
			for strategy in vecMap:
				if(seg in vecMap[strategy]):
					if(length in vecMap[strategy][seg]):
						if(vecMap[strategy][seg][length] < minValue):
							minValue = vecMap[strategy][seg][length]
							minChoice = strategy

			bestValues[seg][length] = minValue
			bestStrategies[seg][length] = minChoice


def create_tex(bestStrategies, dirFiles, equalOrDiff):
	f = open(dirFiles+ "/../" + dirFiles.split('/')[2] + "-" + "Best-" + equalOrDiff + ".tex", 'w')

	f.write("\\begin{table}\n\
	\centering\n\
	\def\\arraystretch{1.2}\n\
	\setlength{\\tabcolsep}{0.1em}\n\
	\scriptsize\n\
	\caption{TESTE}\n\
	\\begin{tabular}\n\
	{|C{0.2cm}C{0.5cm}||C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}|}\n \
	\hhline{|*{15}{-}|}\n\
	&    & \multicolumn{13}{c|}{Array Length ($2^{n}$)} \\\\ \n\
	&    & 15         & 16         & 17         & 18         & 19         & 20         & 21         & 22         & 23         & 24         & 25         & 26         & 27 \\\\ \
	\hhline{|*{15}{=}|}\n\
	\parbox[t]{1pt}{\multirow{21}{*}{\\rotatebox[origin=c]{90}{Number of segments ($2^{m}$)}}}\n")

	seg=1
	while seg <= 1048576:
		length = 32768
		f.write(" & " + str(int(math.log(seg,2))))

		while length <= 134217728:
			if(length/seg <= 1):
				f.write(" & ")
			else:
				f.write(" & \\" + bestStrategies[seg][length])
			length *= 2
		
		seg *= 2
		f.write("\\\\ \n")

	f.write("\hhline{|*{16}{-}|}\n\
	\end{tabular}\n\
	\end{table}\n")
