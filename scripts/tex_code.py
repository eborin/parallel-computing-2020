#!/usr/bin/python3.6

packages = "\
%%\\usepackage{multirow}\n\
%%\\usepackage{makecell}\n\
%%\\usepackage{adjustbox}\n\
%%\\usepackage{hhline}\n\
%%\\usepackage{tabu}\n"

commands = "\
%%\\definecolor{c1}{HTML}{984EA3}\n\
%%\\definecolor{c2}{HTML}{377EB8}\n\
%%\\definecolor{c3}{HTML}{E41A1C}\n\
%%\\definecolor{c4}{HTML}{4DAF4A}\n\
%%\\definecolor{c5}{HTML}{FF7F00}\n\
%%\\definecolor{c6}{HTML}{A65628}\n\
%%\\newcommand{\\bbsegsort}{\\color{c4}H}\n\
%%\\newcommand{\\fixcub}{\\color{c5}FC}\n\
%%\\newcommand{\\fixthrust}{\\color{brown}FT}\n\
%%\\newcommand{\\mergeseg}{\\color{c2}M}\n\
%%\\newcommand{\\radixseg}{\\color{c3}R}\n\
%%\\newcommand{\\nthrust}{\\color{c1}MT}\n\
%%\\newcommand{\\noTest}{-}\n"

def header_best_strategy(caption, machine, equalOrDiff):
	return "\
\\begin{minipage}{.32\\linewidth}\n\
\centering\n\
\def\\arraystretch{0.9}\n\
\setlength{\\tabcolsep}{0.1em}\n\
\\tiny\n\
\caption{Best results for each combination of array length and number of segments considering segments " + caption + "}\n\
\\vspace*{-3mm}\n\
\label{" + machine.lower() + "-" + equalOrDiff +"}\n\
\\begin{tabular}\n\
{|C{0.2cm}C{0.4cm}||C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}C{0.25cm}|}\n \
\hhline{|*{15}{-}|}\n\
&    & \multicolumn{13}{c|}{Array Length ($2^{n}$)} \\\\ \n\
&    & 15         & 16         & 17         & 18         & 19         & 20         & 21         & 22         & 23         & 24         & 25         & 26         & 27 \\\\ \
\hhline{|*{15}{=}|}\n\
\parbox[t]{1pt}{\multirow{21}{*}{\\rotatebox[origin=c]{90}{Number of segments ($2^{m}$)}}}\n"

tail = "\
\hhline{|*{16}{-}|}\n\
\end{tabular}\n\
\end{minipage}\n"

def header_count_best(strategy):
	return "\
\\begin{minipage}{.42\\linewidth}\n\
\centering\n\
\def\\arraystretch{0.9}\n\
\setlength{\\tabcolsep}{0.1em}\n\
\\tiny\n\
\caption{Percentage where \\textbf{\\" + strategy + "} is the best for each combination of array length and number of segments considering all GPUs.}\n\
\\vspace*{-3mm}\n\
\label{count-best-" + strategy + "}\n\
\\begin{tabular}\n\
{|C{0.2cm}C{0.4cm}||C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}|}\n \
\hhline{|*{15}{-}|}\n\
&    & \multicolumn{13}{c|}{Array Length ($2^{n}$)} \\\\ \n\
&    & 15         & 16         & 17         & 18         & 19         & 20         & 21         & 22         & 23         & 24         & 25         & 26         & 27 \\\\ \
\hhline{|*{15}{=}|}\n\
\parbox[t]{1pt}{\multirow{21}{*}{\\rotatebox[origin=c]{90}{Number of segments ($2^{m}$)}}}\n"


def header_the_best():
	return "\
\\begin{table}\n\
\centering\n\
\def\\arraystretch{0.9}\n\
\setlength{\\tabcolsep}{0.1em}\n\
\\scriptsize\n\
\caption{The best strategy for each scenario considering all GPUs results}\n\
\\vspace*{-3mm}\n\
\label{the-best}\n\
\\begin{tabular}\n\
{|C{0.2cm}C{0.4cm}||C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}C{0.45cm}|}\n \
\hhline{|*{15}{-}|}\n\
&    & \multicolumn{13}{c|}{Array Length ($2^{n}$)} \\\\ \n\
&    & 15         & 16         & 17         & 18         & 19         & 20         & 21         & 22         & 23         & 24         & 25         & 26         & 27 \\\\ \
\hhline{|*{15}{=}|}\n\
\parbox[t]{1pt}{\multirow{21}{*}{\\rotatebox[origin=c]{90}{Number of segments ($2^{m}$)}}}\n"


tailTheBest = "\
\hhline{|*{16}{-}|}\n\
\end{tabular}\n\
\end{table}\n"


def header_all_bests():
	return "\
\\begin{table*}\n\
\centering\n\
\def\\arraystretch{0.9}\n\
\setlength{\\tabcolsep}{0.1em}\n\
\\scriptsize\n\
\caption{The best strategies for at least one time in each scenario considering all GPUs results}\n\
\\vspace*{-3mm}\n\
\label{the-best}\n\
\\begin{tabular}\n\
{|C{0.35cm}C{0.32cm}||c|c|c|c|c|c|c|c|c|c|c|c|c|}\n \
\hhline{|*{15}{-}|}\n\
&    & \multicolumn{13}{c|}{Array Length ($2^{n}$)} \\\\ \n\
&    & 15         & 16         & 17         & 18         & 19         & 20         & 21         & 22         & 23         & 24         & 25         & 26         & 27 \\\\ \
\hhline{|*{15}{=}|}\n\
\parbox[t]{1pt}{\multirow{21}{*}{\\rotatebox[origin=c]{90}{Number of segments ($2^{m}$)}}}\n"

tailAllBests = "\
\hhline{|*{15}{-}|}\n\
\end{tabular}\n\
\end{table*}\n"