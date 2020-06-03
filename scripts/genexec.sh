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

function execute_sort_kernel ()
{
    local app="${1}"
    local inp="${2}"
    local id="${3}"
    local time_dir="${4}"
    local err_file="${app}-${in}.err"
    echo "${app} < ${inp}" > "${err_file}" 
    OUT=`"${app}" < ${inp}` 2>> "${err_file}"
    if [ "$?" == 0 ]; then
	rm -f "${err_file}"
	echo "$OUT"      >> "${time_dir}/${id}.time"
	echo "$OUT ; OK" >> "${time_dir}/${id}.time2"
    else
	mv "${err_file}" "${time_dir}/"
	cp "${inp}" "${time_dir}/"
	echo "--"      >> "${time_dir}/${id}.time"
	echo "-- ; ERROR" >> "${time_dir}/${id}.time2"
    fi
}

echo "" > $out/bbsegsort.time
echo "" > $out/mergeseg.time
echo "" > $out/radixseg.time
echo "" > $out/fixcub.time
echo "" > $out/fixthrust.time			
echo "" > $out/fixpasscub.time
echo "" > $out/fixpassthrust.time
echo "" > $out/nthrust.time

echo "" > $out/bbsegsort.time2
echo "" > $out/mergeseg.time2
echo "" > $out/radixseg.time2
echo "" > $out/fixcub.time2
echo "" > $out/fixthrust.time2			
echo "" > $out/fixpasscub.time2
echo "" > $out/fixpassthrust.time2
echo "" > $out/nthrust.time2

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

		echo -e "\n"$s"\n"$n >> $out/bbsegsort.time2
		echo -e "\n"$s"\n"$n >> $out/mergeseg.time2
	  	echo -e "\n"$s"\n"$n >> $out/radixseg.time2
		echo -e "\n"$s"\n"$n >> $out/fixcub.time2
		echo -e "\n"$s"\n"$n >> $out/fixthrust.time2
		echo -e "\n"$s"\n"$n >> $out/fixpasscub.time2
		echo -e "\n"$s"\n"$n >> $out/fixpassthrust.time2

		if [ $s -le 2048 ]; then
			echo -e "\n"$s"\n"$n >> $out/nthrust.time2
		fi
		
		i=1
		while [ $i -le  10 ] 
		do
			in=$s"_"$n"_"$i".in"
			D=`date`
			report "- Executing for in = ${in}. Start at $D"

			./$generator $s $n > $in
			if [ "$?" != 0 ]; then
			    fail "error when executing ./$generator $s $n > $in"
			else
			    for ap in mergeseg radixseg fixcub fixthrust fixpasscub fixpassthrust; do
				execute_sort_kernel "./${ap}.exe" "${in}" "${ap}" "${out}" 
			    done

			    execute_sort_kernel "./bbsegsort/bbsegsort.exe" "${in}" "bbsegsort" "${out}" 

			    if [ $s -le 2048 ]; then
				execute_sort_kernel "./nthrust.exe" "${in}" "nthrust" "${out}"
			    fi
			fi
			
			D=`date`
			report "- Executing for in = ${in}. End at $D"

			rm -f $in
			((i=$i+1))
		done
		((s=$s*2))
		
	done
	((n=$n*2))
done
