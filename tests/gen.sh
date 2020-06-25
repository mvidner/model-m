NAME=0
for B in "0.4" "0.44444444" "0.48888889" "0.53333333" "0.57777778" "0.62222222" "0.66666667" "0.71111111" "0.75555556" "0.8"; do
for R in "0.2" "0.25555556" "0.31111111" "0.36666667" "0.42222222" "0.47777778" "0.53333333" "0.58888889" "0.64444444" "0.7"; do
    A=`bc -l <<< "$B/2"`
    echo $B $R 0$A
    cp template.ini gs_2_$NAME.ini 
    eval sed -i 's/BB/$B/g' gs_2_$NAME.ini 
    eval sed -i 's/RR/$R/g' gs_2_$NAME.ini 
    eval sed -i 's/AA/0$A/g' gs_2_$NAME.ini
    NAME=`expr $NAME + 1`
done
done
