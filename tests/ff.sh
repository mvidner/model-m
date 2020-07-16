#qsub -N quara -q qprod5 -l "select=1:ncpus=110"  -v NAME="newtowndb_quara" run.sh
#qsub -N quara2 -q qprod5 -l "select=1:ncpus=110"  -v NAME="newtowndb_quara2" run.sh
#qsub -N newtown -q qprod5 -l "select=1:ncpus=110"  -v NAME="newtowndb" run.sh

#for B in "0.4"; do  #"0.5" "0.6" "0.7" "0.45" "0.55" "0.65" "0.425" "0.475" "0.525" "0.575" "0.625" "0.675"; do 

for NAME in $@; do

if test -e $NAME.png; then
echo "OK"
else

i=0
for B in $NAME; do
    for I in `seq 0 999`; do
	if test -e history_${B}_$I.csv; then
	    echo -n "+"
	else
#	  echo -n "$I "	
	  echo -n -
	  i=`expr $i + 1` 
	fi
    done
done
echo
echo "missing $i" 
fi
done

