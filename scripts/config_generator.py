#!/usr/bin/python3.6
######################################################################################################################
# Gerar o tex? True or False
texGenerator = True

# Gerar o csv? True or False
csvGenerator = True
######################################################################################################################
# Gerar o csv? True or False
scurveGenerator = True

# Abbreviations of each strategy, used in csv and scurve
abbreviations = {'bbsegsort':'H','mergeseg':'M','radixseg':'R','nthrust':'MT','fixthrust':'FT','fixcub':'FC', '--':'--'}

# Symbols to be plotted in scurve
symbols = {'bbsegsort':'.-','mergeseg':'*-','radixseg':'v-','nthrust':'x-','fixthrust':'m+-','fixcub':'y|-'}

# Colors of each strategy
colors = {'bbsegsort':'green','mergeseg':'blue','radixseg':'red','nthrust':'purple','fixthrust':'brown','fixcub':'orange'}
######################################################################################################################
# Gerar a comparação entre FC e FT? True or False
fixcompGenerator = True

# Simbolos para a geração do gráfico
fixcompSymbols = {'all':'.-','fix':'*-','sort':'v-'}

# Labels para a geração do gráfico
fixcompLabels = {'all':'Fix Sort FC/FT','fix':'Fix FC/FT','sort':'Sort FC/FT'}

# Número de segmentos para a geração do gráfico
fixcomp_seg = 16384
#######################################################################################################################
# Gerar a relação fix pass/fix sort? True or False
fixpassrelGenerator = True

# Simbolos para a geração do gráfico
fixpassrelSymbols = {'fixthrust':'m+-','fixcub':'y|-'}

# Labels para a geração do gráfico
fixpassrelLabels = {'fixcub':'Fix/FC', 'fixthrust':'Fix/FT'}

# Número de segmentos para a geração do gráfico
fixpassrel_seg = 16384
#######################################################################################################################