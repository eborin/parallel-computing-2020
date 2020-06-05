dir=$1

./parser.exe $dir/fixcub.time $dir/00fixcub.time
./parser.exe $dir/fixthrust.time $dir/00fixthrust.time
./parser.exe $dir/mergeseg.time $dir/00mergeseg.time
./parser.exe $dir/radixseg.time $dir/00radixseg.time
./parser.exe $dir/bbsegsort.time $dir/00bbsegsort.time
./parser.exe $dir/fixpassthrust.time $dir/00fixpassthrust.time
./parser.exe $dir/fixpasscub.time $dir/00fixpasscub.time
./parser2048.exe $dir/nthrust.time $dir/00nthrust.time

sed -i 's/\./\,/g' $dir/00fixcub.time
sed -i 's/\./\,/g' $dir/00fixthrust.time
sed -i 's/\./\,/g' $dir/00fixpasscub.time
sed -i 's/\./\,/g' $dir/00fixpassthrust.time
sed -i 's/\./\,/g' $dir/00mergeseg.time
sed -i 's/\./\,/g' $dir/00radixseg.time
sed -i 's/\./\,/g' $dir/00bbsegsort.time
sed -i 's/\./\,/g' $dir/00nthrust.time
