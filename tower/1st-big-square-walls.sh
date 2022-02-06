function ConfirmAll () {
    # sleep 0.2 ; xdotool key --window $WX Escape
    sleep 0.2 ; xdotool key --window $WX KP_Enter
    sleep 0.2 ; xdotool key --window $WX Shift+KP_Enter
    sleep 0.2 ; xdotool key --window $WX Escape
}

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

key Escape w
type "4" 7 "7" 5 "u" 9
ConfirmAll

type "w" 1 "2" 10 "u" 9
ConfirmAll

type "w" 1 "2" 6 "u" 1
ConfirmAll

type "w" 1 "k" 9 "6" 7
ConfirmAll

type "w" 1 "k" 9 "6" 10
ConfirmAll

type "w" 1 "k" 1 "6" 6
ConfirmAll

type "w" 1 "u" 9 "9" 2 "8" 2
ConfirmAll

type "w" 1 "u" 9 "8" 10
ConfirmAll

type "w" 1 "u" 1 "8" 6
ConfirmAll

type "w" 1 "k" 9 "7" 1 "4" 5
ConfirmAll

type "w" 1 "k" 9 "4" 10
ConfirmAll

type "w" 1 "k" 1 "4" 6
ConfirmAll

type "f" 1 "3" 9 "2" 1
