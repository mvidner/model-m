# ID="no_policy"
# for SUFFIX in  "roman" "petra" "petra_light"; do
#     for I in `seq  0 9`; do
# 	python run_experiment.py -r  village0_${SUFFIX}.ini ${ID}_${SUFFIX}_$I > ${ID}_${SUFFIX}_$I.log &
#     done
# done 

# ID="strong_policy"
# for SUFFIX in  "roman" "petra" "petra_light"; do
#     for I in `seq  0 9`; do
# 	python run_experiment.py -r  -p strong_policy village0_${SUFFIX}.ini ${ID}_${SUFFIX}_$I > ${ID}_${SUFFIX}_$I.log &
#     done
# done 

ID="weighted_policy"
for SUFFIX in  "roman" "petra" "petra_light"; do
    for I in `seq  0 9`; do
	python run_experiment.py -r  -p weighted_policy village0_${SUFFIX}.ini ${ID}_${SUFFIX}_$I > ${ID}_${SUFFIX}_$I.log &
    done
done 


