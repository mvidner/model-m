#qsub -N seirsplus_quarantine -q qgpulong -l "select=1" -v FILE="seirplus_exampleQ.ini",ID="seirsplus_quarantine" run_task.pbs
#qsub -N seirsplus_no_policy -q qgpulong -l "select=1" -v FILE="seirplus_example.ini",ID="seirsplus_no_policy" run_task.pbs
# qsub -N village0_no_policy -q qgpulong -l "select=1" -v FILE="chocerady.ini",ID="village0_no_policy" run_task.pbs
qsub -N village0_strong_quarantine -q qgpulong -l "select=1" -v FILE="village0.ini",ID="village0_strong_quarantine",P="-p" run_task.pbs
