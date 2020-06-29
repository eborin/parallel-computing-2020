#!/usr/bin/python3.6

# Abbreviations of each strategy, used in csv and scurve
abbreviations = {'bbsegsort':'H','mergeseg':'M','radixseg':'R','nthrust':'MT','fixthrust':'FT','fixcub':'FC'}

# Symbols to be plotted in scurve
symbols = {'bbsegsort':'.-','mergeseg':'*-','radixseg':'v-','nthrust':'x-','fixthrust':'m+-','fixcub':'y|-'}

# Colors of each strategy
colors = {'bbsegsort':'green','mergeseg':'blue','radixseg':'red','nthrust':'purple','fixthrust':'brown','fixcub':'orange'}

# Gerar o csv? True or False
texGenerator = False

# Gerar o csv? True or False
csvGenerator = True

# Gerar o csv? True or False
scurveGenerator = True