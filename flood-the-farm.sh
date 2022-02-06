function key () {
    XG="$1"
    shift
    while [ ! -z "$1" ] ; do
        sleep 0.5 ; xdotool key --window $XG $1
        shift
    done
}


SIZE=7
OTHER=5
for j in $(seq 0 $OTHER)
do

    for i in $(seq 0 $SIZE)
    do
        #key $DF Return
        key $WX Shift+Right
    done

    key $WX Shift+Down

    for i in $(seq 0 $SIZE)
    do
        key $WX Shift+Left
    done
    key $WX Shift+Down
done
