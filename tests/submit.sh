# qsub -N barabasi_quarantine -q qgpulong -l "select=1" -v FILE="seirplus_example.ini",ID="barabasi_quarantine",P="-p" run_task.pbs
# qsub -N barabasi_no_policy -q qgpulong -l "select=1" -v FILE="seirplus_example.ini",ID="barabasi_no_policy",P="" run_task.pbs
# qsub -N village0_no_policy -q qgpulong -l "select=1" -v FILE="chocerady.ini",ID="village0_no_policy" run_task.pbs
#qsub -N village0_strong_quarantine -q qgpulong -l "select=1" -v FILE="village0.ini",ID="village0_strong_quarantine",P="-p" run_task.pbs
# qsub -N normal_life -q qgpulong -l "select=1:ncpus=10" -v FILE="town0.ini",ID="normal_life",P="" run_task.pbs
#qsub -N closed_friends -q qgpulong -l "select=1:ncpus=10" -v FILE="town0_closed_friends.ini",ID="closed_friends",P="" run_task.pbs
#qsub -N postprocessing -q qgpulong -l "select=1:ncpus=1" make_plot.sh
# qsub -N normal_life -q qgpulong -l "select=1:ncpus=10" -v FILE="town0_short.ini",ID="normal_life_100",P="" run_task.pbs
# qsub -N closed_schools -q qgpulong -l "select=1:ncpus=10" -v FILE="town0_closed_schools_short.ini",ID="closed_schools_100",P="" run_task.pbs
# qsub -N normal_life -q qgpulong -l "select=1:ncpus=8" -v FILE="town0.ini",ID="normal_life",P="" run_task.pbs
# qsub -N closed_schools -q qgpulong -l "select=1:ncpus=8" -v FILE="town0_closed_schools.ini",ID="closed_schools",P="" run_task.pbs
# qstat
#qsub -N normal_life -q qgpulong -l "select=1:ncpus=8" -v FILE="village0.ini",ID="village_normal_life",P="" run_task.pbs
#qsub -N closed_schools -q qgpulong -l "select=1:ncpus=8" -v FILE="village0_closed_schools.ini",ID="village_closed_schools",P="" run_task.pbs

function run {
#    qsub -N town0 -q qgpulong -l "select=1:ncpus=$1" -v INTERVAL="$2",FILE="town0_closed_schools.ini",ID="closed_schools",P="" run_task.pbs
#    name=`echo -n $3 | sed 's/ /\_/g'`
    L=`echo $2 | sed 's/ /_/g'`
#    qsub -N "town0_${1}_$L" -q qprod -l "select=1:ncpus=$1" -v INTERVAL="$2",FILE="town0_closed_schools.ini",TID="closed_schools",P="" run_task.pbs
    qsub -N "town0_${1}_$L" -q qprod5 -l "select=1:ncpus=$1" -v INTERVAL="$2",FILE="town0.ini",TID="normal_life",P="" run_task.pbs
}

#for B in 9;
#do
N=8
MAX=100
START=0
while test $((START + N)) -le $MAX; do
    run $N "$START `expr $START + $N - 1`" 
    let "START+=N"
done
if test $START -le $MAX; then 
    run $N "$START $MAX" 
fi
#done
qstat
