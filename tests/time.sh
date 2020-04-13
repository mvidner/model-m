for POLICY in "no_policy" "strong_policy" "weighted_policy"; do

    echo "roman,petra,petra_light" > $POLICY.csv 
    for I in `seq 0 9`; do
	for GRAPH in "roman" "petra" "petra_light"; do
	    T=`tail -n 1 ${POLICY}_${GRAPH}_$I.log`
	    echo -n "$T,"   >> $POLICY.csv 
	done
	echo >> $POLICY.csv 
    done  
done
