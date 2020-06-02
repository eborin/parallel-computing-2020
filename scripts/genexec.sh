#!/bin/bash
out=$1
generator=$2

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
			./$generator $s $n > $in

			./bbsegsort/bbsegsort.exe 	< $in 	>> $out/bbsegsort.time
			./mergeseg.exe 			< $in 	>> $out/mergeseg.time
			./radixseg.exe 			< $in 	>> $out/radixseg.time
			./fixcub.exe 			< $in 	>> $out/fixcub.time
			./fixthrust.exe 		< $in	>> $out/fixthrust.time
			./fixpasscub.exe		< $in	>> $out/fixpasscub.time
			./fixpassthrust.exe		< $in	>> $out/fixpassthrust.time

			if [ $s -le 2048 ]; then
				./nthrust.exe			< $in	>> $out/nthrust.time
			fi

			rm -f $in
			((i=$i+1))
		done
		((s=$s*2))
		
	done
	((n=$n*2))
done
