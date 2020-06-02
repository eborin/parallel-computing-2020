#!/bin/bash
out=$1
generator=$2

function report {
    echo "$@"
}

function fail {
    echo "genexec.sh ERROR: $@"
    exit 1
}

echo "" > $out/bbsegsort.time
echo "" > $out/mergeseg.time
echo "" > $out/radixseg.time
echo "" > $out/fixcub.time
echo "" > $out/fixthrust.time			
echo "" > $out/fixpasscub.time
echo "" > $out/fixpassthrust.time
echo "" > $out/nthrust.time

n=32768
while [ $n -le 134217728 ]
do
	s=1
	while [[ $s -lt $n && $s -le 1048576 ]] 
	do
		echo -e "\n"$s"\n"$n >> $out/bbsegsort.time
		echo -e "\n"$s"\n"$n >> $out/mergeseg.time
	  	echo -e "\n"$s"\n"$n >> $out/radixseg.time
		echo -e "\n"$s"\n"$n >> $out/fixcub.time
		echo -e "\n"$s"\n"$n >> $out/fixthrust.time
		echo -e "\n"$s"\n"$n >> $out/fixpasscub.time
		echo -e "\n"$s"\n"$n >> $out/fixpassthrust.time

		if [ $s -le 2048 ]; then
			echo -e "\n"$s"\n"$n >> $out/nthrust.time
		fi
		
		i=1
		while [ $i -le  10 ] 
		do
			in=$s"_"$n"_"$i".in"
			report "- Executing for in = ${in}"
			./$generator $s $n > $in \
			    || fail "error when executing ./$generator $s $n > $in"
			./bbsegsort/bbsegsort.exe < $in >> $out/bbsegsort.time \
			    || fail "error when executing bbsegsort/bbsegsort.exe < $in"
			./mergeseg.exe 			< $in 	>> $out/mergeseg.time \
			    || fail "error when executing mergeseg.exe < $in"
			./radixseg.exe 			< $in 	>> $out/radixseg.time \
			    || fail "error when executing radixseg.exe < $in"
			./fixcub.exe 			< $in 	>> $out/fixcub.time \
			    || fail "error when executing fixcub.exe < $in"
			./fixthrust.exe 		< $in	>> $out/fixthrust.time \
			    || fail "error when executing fixthrust.exe < $in"
			./fixpasscub.exe		< $in	>> $out/fixpasscub.time \
			    || fail "error when executing fixpasscub.exe < $in"
			./fixpassthrust.exe		< $in	>> $out/fixpassthrust.time \
			    || fail "error when executing fixpassthrust.exe < $in"

			if [ $s -le 2048 ]; then
				./nthrust.exe	       	< $in	>> $out/nthrust.time \
				    || fail "error when executing nthrust.exe < $in"
			fi

			rm -f $in
			((i=$i+1))
		done
		((s=$s*2))
		
	done
	((n=$n*2))
done
