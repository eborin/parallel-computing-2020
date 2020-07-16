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
#######################################################################################################################
# Gerar gráfico de tempo do Fix? True or False
fixtimesGenerator = True

# Número de segmentos para a geração do gráfico
fixtimes_seg = 32768
######################################################################################################################
# Gerar a comparação entre FC e FT? True or False
fixspeedupGenerator = True

# Simbolos para a geração do gráfico
fixspeedupSymbols = {'all':'.-','fix':'*-','sort':'v-'}
fixspeedupSymbolsCalc = ['v--','^--','.-']
fixspeedupColors = {'all':'green','fix':'blue','sort':'red'}

# Labels para a geração do gráfico
fixspeedupLabels = {'all':'Fix Sort FC/FT','fix':'Fix FC/FT','sort':'Sort FC/FT'}
fixspeedupLabelsCalc = ['Min ','Max ','Average ']

# Número de segmentos para a geração do gráfico
fixspeedup_seg = 16384
#######################################################################################################################
# Gerar a relação fix pass/fix sort? True or False
fixstepsGenerator = True

# Simbolos para a geração do gráfico
fixstepsSymbols = {'fixthrust':'m+-','fixcub':'y|-'}

# Labels para a geração do gráfico
fixstepsLabels = {'fixcub':'Fix/FC', 'fixthrust':'Fix/FT'}

# Número de segmentos para a geração do gráfico
fixsteps_seg = 16384
#######################################################################################################################
# Gerar hou curve? True or False
houGenerator = True
