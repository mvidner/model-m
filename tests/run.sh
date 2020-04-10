ID="no_policy"
for I in `seq  0 9`; do
    python run_experiment.py -r romeo_and_juliet.ini ${ID}_$I > ${ID}_$I.log 
done

ID="quarantine"
for I in `seq  0 9`; do
    python run_experiment.py -r romeo_and_julietQ.ini ${ID}_$I > ${ID}_$I.log 
done
