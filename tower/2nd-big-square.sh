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

key Escape f
type "4" 2 "7" 10 "7" 4 "2" 1
type "uk" 9
ConfirmAll

key f
type "uk" 8 "k" 1
type "6" 9 "9" 1
ConfirmAll

key f
type "uk" 8 "k" 1
type "6" 10
ConfirmAll

key f
type "u" 8 "k" 3
type "6" 7
ConfirmAll

key f
type "uk" 9
type "6" 7 "2" 1
ConfirmAll

key f
type "uk" 9
type "2" 10
ConfirmAll

key f
type "uk" 7 "k" 2
type "2" 9
ConfirmAll

key f
type "uk" 9 "2" 9
ConfirmAll

key f
type "uk" 8 "k" 1 "4" 1 "4" 9
ConfirmAll

key f
type "uk" 8 "k" 1 "4" 10
ConfirmAll

key f
type "u" 8 "k" 3 "4" 7
ConfirmAll

key f
type "uk" 9 "4" 7
ConfirmAll

key f
type "uk" 9 "8" 10
ConfirmAll

key f
type "uk" 7 "k" 2 "8" 9
ConfirmAll

key f
type "6" 12 "3" 4
