function type () {
    XG="$1"
    shift
    while [ ! -z "$1" ] ; do
        if [ -z "$2" ] ; then
            sleep 0.2 ; xdotool type --window $XG --delay 200 $1
            shift
        else
            for i in $(seq 1 $2) ; do
                sleep 0.2 ; xdotool type --window $XG --delay 200 $1
            done
            shift
            shift
        fi
    done
}

function key () {
    XG="$1"
    shift
    while [ ! -z "$1" ] ; do
        sleep 0.2 ; xdotool key --window $XG $1
        shift
    done
}


echo "$DH"

while true
do

key $DH Up
key $DH Return
key $WX Down
#key $WX Return
#key $WX Return
#key $WX Down

done
