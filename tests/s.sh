#qsub -N run.sh -q qprod5 -l "select=1:ncpus=110"  run.sh
#qsub -N run.sh -q qprod5 -l "select=1:ncpus=110"  run.sh
#qsub -N run.sh -q qprod5 -l "select=1:ncpus=110"  multirun.sh

#qsub -N vanilla_fitted -q qprod5 -l "select=1:ncpus=100" -v NAME="vanilla_fitted_no_policy" multirun.sh#
#qsub -N presentation_obr -q qprod5 -l "select=1:ncpus=110" -v NAME="half_eva_dusek",NJ=100 multirun.sh
#qsub -N presentation_obr -q qprod5 -l "select=1:ncpus=110" -v NAME="super_eva_dusek",NJ=100 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="no_reduction_no_close_dusek",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod5 -l "select=1:ncpus=110" run.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="no_eva_dusek",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="half_eva_dusek",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="super_eva_dusek",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="no_close_dusek",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="baseline_dusek",NJ=40 multirun.sh
#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="no_eva_dusek",NJ=40 multirun.sh

#qsub -N presentation_obr -q qprod1234 -l "select=1:ncpus=44" -v NAME="baseline_dusek2",NJ=40 multirun.sh

#qsub -N test_multi -q qprod1234 -l "select=1:ncpus=44" -v NAME="baseline1115",NJ=40 multirun.sh
ZADANI=$1
qsub -N $ZADANI -q qprod5 -l "select=1:ncpus=125" -v NAME="$ZADANI",NJ=80 multirun.sh
#qsub -N $ZADANI -q qprod1234 -l "select=1:ncpus=44" -v NAME="$ZADANI",NJ=40 multirun.sh
#qsub -N test_multi -q qprod1234 -l "select=1:ncpus=44" -v NAME="b1542",NJ=40 multirun.sh
#qsub -N test_multi -q qprod1234 -l "select=1:ncpus=44" -v NAME="b1543",NJ=40 multirun.sh
#qsub -N test_multi -q qprod1234 -l "select=1:ncpus=44" -v NAME="b1544",NJ=40 multirun.sh


#qsub -N presentation_obr -q qprod5 -l "select=1:ncpus=110" -v NAME="baseline_dusek",NJ=100 multirun.sh

#qsub -N presentation_obr -q qprod5 -l "select=1:ncpus=110" -v NAME="no_reduction_no_close_dusek",NJ=100 multirun.sh

#qsub -N sour_fitted -q qprod5 -l "select=1:ncpus=105" -v NAME="sour_fitted" multirun.sh

#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="0 99" run.sh
#sub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="100 199" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="200 299" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="300 399" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="400 499" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="500 599" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="680 699" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="780 799" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="800 899" run.sh
#qsub -N run.sh -q qprod1234 -l "select=1:ncpus=30" -v INTERVAL="900 999" run.sh

#qsub -N quara2 -q qprod5 -l "select=1:ncpus=110"  -v NAME="newtowndb_quara2" run.sh
#qsub -N newtown -q qprod5 -l "select=1:ncpus=110"  -v NAME="newtowndb" run.sh

#for B in "0.4" "0.5" "0.6" "0.7" "0.45" "0.55" "0.65" "0.425" "0.475" "0.525" "0.575" "0.625" "0.675"; do 
#qsub -N newtown$B -q qprod5 -l "select=1:ncpus=110"  -v NAME="newtown_$B" run.sh
#done
