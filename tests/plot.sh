unzip history_$1.zip 
python plot_cmp.py $1 $1
rm history_$1_*.csv durations_$1_*.csv
