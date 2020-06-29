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

def header(caption):
	return "\
\\begin{table}\n\
\centering\n\
\def\\arraystretch{1.2}\n\
\setlength{\\tabcolsep}{0.1em}\n\
\scriptsize\n\
\caption{Best results for each combination of array length and number of segments considering segments " + caption + "}\n\
\\begin{tabular}\n\
{|C{0.2cm}C{0.5cm}||C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}C{0.51cm}|}\n \
\hhline{|*{15}{-}|}\n\
&    & \multicolumn{13}{c|}{Array Length ($2^{n}$)} \\\\ \n\
&    & 15         & 16         & 17         & 18         & 19         & 20         & 21         & 22         & 23         & 24         & 25         & 26         & 27 \\\\ \
\hhline{|*{15}{=}|}\n\
\parbox[t]{1pt}{\multirow{21}{*}{\\rotatebox[origin=c]{90}{Number of segments ($2^{m}$)}}}\n"

tail = "\
\hhline{|*{16}{-}|}\n\
\end{tabular}\n\
\end{table}\n"