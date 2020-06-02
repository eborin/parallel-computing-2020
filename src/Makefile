#TIME=1
#BITS=12
#EXECS=1
#STREAMS=32
#ARCH=52

arch= -gencode arch=compute_${ARCH},code=sm_${ARCH} -O3

all: mergeseg radixseg fixcub fixthrust fixpasscub fixpassthrust nthrust 

mergeseg: mergeseg.cu
	nvcc $(arch) mergeseg.cu -o mergeseg.exe -I"../lib" -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS) -Xptxas="-v"

radixseg: radixseg.cu
	nvcc $(arch) radixseg.cu -o radixseg.exe -I"../lib" -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS)

fixcub: fixcub.cu
	nvcc $(arch) fixcub.cu -o fixcub.exe -I"../lib" -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS)

fixpasscub: fixpasscub.cu
	nvcc $(arch) fixpasscub.cu -o fixpasscub.exe -I"../lib" -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS)
 
fixthrust: fixthrust.cu
	nvcc $(arch) fixthrust.cu -o fixthrust.exe -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS)

fixpassthrust: fixpassthrust.cu
	nvcc $(arch) fixpassthrust.cu -o fixpassthrust.exe -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS)

newthrustthr: newthrust.cu
	nvcc -ccbin g++ -Xcompiler -fopenmp $(arch) newthrust.cu -o newthrust$(STREAMS)thr.exe -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS) -DNUM_STREAMS=$(STREAMS) -DTHREADS

newthrustschedthr: newthrust.cu
	nvcc -ccbin g++ -Xcompiler -fopenmp $(arch) newthrust.cu -o newthrust$(STREAMS)schedthr.exe -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS) -DNUM_STREAMS=$(STREAMS) -DSCHEDULE -DTHREADS

nthrust: nthrust.cu
	nvcc $(arch) nthrust.cu -o nthrust.exe -std=c++11 --expt-extended-lambda -lcuda -DELAPSED_TIME=$(TIME) -DEXECUTIONS=$(EXECS)
	
