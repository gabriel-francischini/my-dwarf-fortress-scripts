import sys
sys.path.append('')

from image_engine import do_image, no_move, no_start, no_draw, no_exit
from image_engine import print_move, print_start, print_draw, print_exit
from image_engine import Coordinate, Rectangle

df_wpid = int($(wmctrl -lp | grep -i 'Dwarf Fortress').split(' ')[0], 16)

WX = str(df_wpid)
echo "Dwarf Fortress is runnning at: " @(WX) " ."


VERBOSITY = 1
def print_verbose(string, level):
    if VERBOSITY >= level:
        print(f'        v{level}' + '    ' * level + string)

verbose   = lambda s: print_verbose(s, 1)
vverbose  = lambda s: print_verbose(s, 2)
v3verbose = lambda s: print_verbose(s, 3)
v4verbose = lambda s: print_verbose(s, 4)
v5verbose = lambda s: print_verbose(s, 5)

def xtype(string):
    global WX
    v3verbose(f"Typing {string.__repr__()}")
    if string == '':
        return

    if type(string) == str and len(string) == 1:
        sleep 0.1 ;xdotool type --window @(WX) --delay 30  @(string)
    else:
        for i in string:
            xtype(i)

def xkey(string):
    global WX
    v3verbose(f"Keying {string.__repr__()}")
    if type(string) == str:
        sleep 0.1 ; xdotool key --window @(WX) @(string)
    else:
        for i in string:
            xkey(i)

ESC = 'Escape'
Ret = 'Return'
Enter = 'KP_Enter'
Shift_Enter = 'Shift+KP_Enter'


versor_to_str = {
    (-1, -1): '7', (0, -1): '8', (1, -1): '9',
    (-1,  0): '4', (0,  0): '5', (1,  0): '6',
    (-1,  1): '1', (0,  1): '2', (1,  1): '3',
}

versor_to_10_str = {k: v for k, v in versor_to_str.items()}
update = {
    (0, -1): 'KP_Up',
    (0,  1): 'KP_Down',
    (-1, 0): 'KP_Left',
    (1,  0): 'KP_Right',
}

for k in update:
    versor_to_10_str[k] = update[k]

str_to_versor = {v: k for (k, v) in versor_to_str.items()}

def get_versor(iterable, multiplier=1):
    def l(v):
        if v == 0:
            return 0
        else:
            return multiplier * abs(v) / v

    return tuple(map(l, iterable))

def move(_from, to):
    print_move(_from, to)
    fx, fy = _from
    tx, ty = to
    dx, dy = tx - fx, ty - fy

    to_type = ''
    while dx != 0 or dy != 0:
        ux, uy = get_versor((dx, dy))
        v3verbose(f'vars:\n\t{(dx, dy)=}\n\t{(ux, uy)=}')

        while abs(dx) > 6 or abs(dy) > 6:
            ux = ux if abs(dx) > 5 else 0
            uy = uy if abs(dy) > 5 else 0
            xkey('Shift+' + versor_to_10_str[(ux, uy)])
            dx -= 11 * ux
            dy -= 11 * uy
            ux, uy = get_versor((dx, dy))
            v3verbose(f'vars:\n\t{(dx, dy)=}\n\t{(ux, uy)=}')

        while abs(dx) > 0 or abs(dy) > 0:
            to_type += versor_to_str[(ux, uy)]
            dx -= ux
            dy -= uy
            ux, uy = get_versor((dx, dy))
            v3verbose(f'vars:\n\t{(dx, dy)=}\n\t{(ux, uy)=}')

    xtype(to_type)
    return tx + int(dx), ty + int(dy)

def draw_by_placebo(p: Coordinate, r: Rectangle) -> Coordinate:
    (start, end) = r
    v5verbose(f'Draw by placebo: {(p, r)=}\t{(start, end)=}')

    print_draw(p, r)

    if p != start:
        verbose(f'To draw {(p, r)=} we move {(p, start)=}')
        p = move(p, start)

    if p != end:
        verbose(f'To keep drawing, we move {(p, end)=}')
        p = move(p, end)

    return p

def start_by_placebo(p: Coordinate, r: Rectangle) -> Coordinate:
    print(f'Start by placebo: {(p, r)=}')
    start, end = r
    print_start(p, r)
    return draw_by_placebo(p, r)


def resize_rect():
    u_moves = {
        1: 0,
        2: 1, 3: 1,
        4: 2, 5: 2,
        6: 3, 7: 3,
        8: 4, 9: 4,
        10: 5
    }

    k_moves = {
        1: 0,
        2: 1, 3: 1,
        4: 2, 5: 2,
        6: 3, 7: 3,
        8: 4, 9: 4,
        10: 5
    }

fp = '/home/gabriel/Downloads/LinuxLNP-0.44.12-r03/my-py-scripts/xonsh-scripts/example.png'

do_image(fp,
         {(255, 255, 255): (no_draw, no_draw, print_exit),
          (0, 255, 0): (start_by_placebo, draw_by_placebo, print_exit),
         },
         (255, 255, 0),
         move)
