for N in $@; do
    unzip history_$N.zip 
done 

python plot_all.py cmp $@ 'title'
#python plot_test.py cmp2 $@


for N in $@; do
    rm history_${N}_*.csv durations_${N}_*.csv
done
