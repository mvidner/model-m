#for I in `seq 0 99`; do
#    python run_experiment.py -r  town0.ini no_policy_start10_$I > no_policy_start10_$I.log &
#    pids[${I}]=$!
#done

# wait for all pids
#for pid in ${pids[*]}; do
# 	wait $pid
#done
#unset pids

function wait_for_finished {
    while true; do
	C=`pgrep -c python`
	if test $C -lt 45; then
	    break
	fi 
	sleep 1m
    done
}


#NAME=newtown
#INTERVAL="0 19"

for NAME in "plain_vanilla_fitted"; do
ID=$NAME
for I in `seq 0 99`; do
    wait_for_finished
    python -OO run_experiment.py -r ${NAME}.ini ${ID}_$I > ${ID}_$I.log  2> ${ID}_$I.err &
    sleep 1s
    pids[${I}]=$!
done
for pid in ${pids[*]}; do
 	wait $pid
done
unset pids
done
 

