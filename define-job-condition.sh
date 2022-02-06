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

type "c" #p
type "n" #qqn
type "500"
key Return Escape Down
