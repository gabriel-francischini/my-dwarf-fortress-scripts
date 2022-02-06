function type () {
    while [ ! -z "$1" ] ; do
        if [ -z "$2" ] ; then
            sleep 0.2 ; xdotool type --window $WX --delay 200 $1
            shift
        else
            for i in $(seq 1 $2) ; do
                sleep 0.2 ; xdotool type --window $WX --delay 200 $1
            done
            shift
            shift
        fi
    done
}

function key () {
    while [ ! -z "$1" ] ; do
        sleep 0.2 ; xdotool key --window $WX $1
        shift
    done
}


PLOT_W=5
PLOT_H=2
PLOT_DW=$(expr $PLOT_W - 1)
PLOT_DH=$(expr $PLOT_H - 1)

ROWS=15
COLUMNS=6


key Escape p

for i in $(seq 1 $ROWS)
do
    for j in $(seq 1 $COLUMNS)
    do

        type "k" $PLOT_DW "u" $PLOT_DH
        key Return p
        type "6" $PLOT_W
    done

    for j in $(seq 1 $COLUMNS)
    do
        type "4" $PLOT_W
    done

    type "2" $PLOT_H
done
