#for I in `seq 0 99`; do
#    python run_experiment.py -r  town0.ini no_policy_start10_$I > no_policy_start10_$I.log &
#    pids[${I}]=$!
#done

# wait for all pids
#for pid in ${pids[*]}; do
# 	wait $pid
#done
#unset pids



#NAME=newtown
#INTERVAL="0 19"

#for NAME in "baseline_with_june" "baseline" "super_eva" "no_eva" "super_eva_with_june" "no_eva_with_june"; do
#for NAME in "plain_vanilla" "sour"; do
ID=$NAME
python -OO run_all.py -r --n_repeat 1000 --n_jobs $NJ ${NAME}.ini ${ID} > ${ID}.log  2> ${ID}.err 

zip history_${NAME}.zip history_${NAME}_*.csv 
rm history_${NAME}_*.csv 
#python plot_cmp.py no_eva_story no_eva_story
 

