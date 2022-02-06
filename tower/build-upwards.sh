xdotool key --window $WX space
sleep 0.2
xdotool type --window $WX --delay 200 "bCf"
WX=$WX ./1st-doors.sh
sleep 0.2
xdotool type --window $WX "<"
WX=$WX ./1st-stair.sh
xdotool key --window $WX Escape
sleep 0.2
xdotool key --window $WX Escape
sleep 0.2
xdotool key --window $WX Escape
sleep 0.2
xdotool key --window $WX space
