qsub -N verona_qurantine -q qgpulong -l "select=1" -v FILE="romeo_and_julietQ.ini",ID="verona_qurantine" run_task.pbs
qsub -N verona_no_policy -q qgpulong -l "select=1" -v FILE="romeo_and_juliet.ini",ID="verona_no_policy" run_task.pbs
