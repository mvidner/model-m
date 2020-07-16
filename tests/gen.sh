NAME=0
for A in "0.5" "0.6" "0.7"; do
for R in "0.5" "0.6" "0.7"; do
for T in "0.2" "0.3" "0.4" "0.5" "0.6"; do
for B in "0.1" "0.15" "0.2" "0.25"; do
    RA=0`bc -l <<< "$B * $A"`
    echo $B $R $RA
    cp template_constanttheta.ini gs_cts_$NAME.ini 
    eval sed -i 's/BB/$B/g' gs_cts_$NAME.ini 
    eval sed -i 's/RR/$R/g' gs_cts_$NAME.ini 
    eval sed -i 's/AA/$RA/g' gs_cts_$NAME.ini
    eval sed -i 's/TT/$T/g' gs_cts_$NAME.ini
    NAME=`expr $NAME + 1`
done
done
done
done
