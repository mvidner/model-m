ID="test"
for I in `seq  0 9`; do
    python run_experiment.py -r example.ini  ${ID}_$I > ${ID}_$I.log &
done
