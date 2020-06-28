NAME=$1
NJ=$2

ID=$NAME
python -OO run_all.py -r --n_repeat 1000 --n_jobs $NJ ${NAME}.ini ${ID} > ${ID}.log  2> ${ID}.err 


python plot_cmp.py ${NAME} ${NAME} 
zip history_${NAME}.zip history_${NAME}_*.csv durations_${NAME}_*.csv
rm history_${NAME}_*.csv durations_${NAME}_*.csv
 

