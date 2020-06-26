prog=$1
file=$2

./${prog} < ${file}
if [ "$?" == 0 ]; then
	echo "OK"
else
	echo "NOT OK"
fi
