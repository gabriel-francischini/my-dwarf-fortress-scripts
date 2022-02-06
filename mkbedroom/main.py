filename = "40lx40l.png"

from PIL import Image
import re

im = Image.open(filename)
im = im.convert('RGB')
im_width, im_height = im.size


points_to_dig = []
starter_point = None


for x in range(0,im_width):
    for y in range(0,im_height):
        pos = (x, y)
        tgt = im.getpixel(pos)
        if (0, 0, 0) == tgt:
            points_to_dig.append(pos)
        elif (127, 127, 127) == tgt:
            starter_point = pos



points_to_dig = set(points_to_dig)


possible_lines = []

for point in points_to_dig:
    directions = [
        (0, 1),
        (1, 0),
        #(0, -1),
        #(-1, 0)
        ]
    def step_in_direction(direction, point):
        return tuple(map(lambda x, y: x+y, direction, point))

    for direction in directions:
        line = []
        cur = point

        while cur in points_to_dig:
            line.append(cur)
            cur = step_in_direction(direction, cur)

        possible_lines.append(line)


points_digged = set()
actual_lines = []
Key = lambda x: (sum([1 if i not in points_digged
                      else -9999 if i not in points_to_dig
                      else 0
                      for i in x])
                 )

possible_lines.sort(key=Key, reverse=True)

while len(possible_lines) > 0:
    line = possible_lines.pop(0)
    [points_digged.add(point) for point in line]
    actual_lines.append(line)
    possible_lines = [x for x in possible_lines
                      if Key(x) > 0]
    possible_lines.sort(key=Key, reverse=True)

#print(points_to_dig - points_digged)

def distance(point_a, point_b):
    d_x = abs(point_a[0] - point_b[0])
    d_y = abs(point_a[1] - point_b[1])
    return d_x ** 2 + d_y ** 2


route = [[starter_point]]
cur = starter_point

while len(actual_lines) > 0:
    actual_lines.sort(key=lambda x: min([distance(cur, x[0]),
                                        distance(cur, x[-1])]))
    next_l = actual_lines.pop(0)
    if distance(cur, next_l[-1]) < distance(cur, next_l[0]):
        next_l = next_l[::-1]
    route.append(next_l)
    cur = next_l[-1]


def str_distance(point_a, point_b):
    Str = ''
    d_x = point_b[0] - point_a[0]
    d_y = point_b[1] - point_a[1]
    if d_x < 0:
        Str += abs(d_x) * '4'
    else:
        Str += d_x * '6'
    if d_y < 0:
        Str += abs(d_y) * '8'
    else:
        Str += d_y * '2'

    return Str

import json
def pprint(x):
    print(json.dumps(x, indent=4, sort_keys=True))

#pprint(route)

result = ''
cur = route.pop(0)[0] # starter_point
while len(route) > 0:
    line = route.pop(0)
    # Travel to line starter_point
    result += str_distance(cur, line[0])
    # Digs the line
    result += "\n"
    result += str_distance(line[0], line[-1])
    result += "\n"
    cur = line[-1]


pim = im.load()
for x in range(im_width):
    for y in range(im_height):
        if (x,y) != starter_point:
            im.putpixel((x, y), (255, 255, 255))


cur_x, cur_y = starter_point
digging = False
counter = 0
shade = 255
shade_r = 255
for char in result:
    if char == '\n':
        if digging == True:
            im.putpixel((cur_x, cur_y), (shade_r, shade, 0))
        digging = not digging
        counter -= 20
        shade = counter % 256
        shade_r = int(counter / 256) % 256
    elif char in '4862':
        if digging == True:
            im.putpixel((cur_x, cur_y), (0, shade, 0))
        if char == '4':
            cur_x -= 1
        elif char == '6':
            cur_x += 1
        elif char == '8':
            cur_y -= 1
        elif char == '2':
            cur_y += 1
    else:
        print(char)

im.save(filename + '_out.png')

def printable(x,p=True):
    z = x.replace('\n', r'\n')
    if p:
        print(z)
    return z

for direction in '2486':
    reg = r'\n([' + direction + r']+)\n\n([' + direction + r']+)\n'
    sub = r'\n\1\2\n'
    #print(reg)
    #print(sub)
    #match = re.search(reg, result)
    #if match:
    #    printable(result[match.start():match.end()])
    #    printable(match.expand(sub))

result = (printable(result, p=False)
          .replace(r'\n',
                   '"\nsleep 0.15 ; xdotool key --window $WX Return'
                   '\n'
                   'xdotool type --window $WX --delay 150 "'))

# for direction in '2486':
#     repl = {'8': 'Shift+Up',
#             '2': 'Shift+Down',
#             '4': 'Shift+Left',
#             '6': 'Shift+Right'}
#     result = result.replace(10 * direction,
#                    '"\nsleep 0.15; xdotool key --window $WX {}'.format(repl[direction]) +
#                    '\n'
#                    'xdotool type --window $WX --delay 150 "')
# result = result.replace('\nxdotool type --window $WX --delay 150 ""\n', '\n')
print('WX=117440526\n\nxdotool type --window $WX "' + result)
