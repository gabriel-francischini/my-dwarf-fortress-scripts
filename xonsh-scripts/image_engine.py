from PIL import Image, ImageDraw
import re
from typing import List, Set, Dict, Tuple, Optional, Any, Generic
from typing import Callable, Iterator, Union, Optional, List, Sequence, TypeVar
import random


# see: https://github.com/python/mypy/issues/8278
Val = TypeVar("Val")
class Parametrizable(Generic[Val]):
    def __init__(self, a: Val): ...

T, U, V, W = TypeVar('T'), TypeVar('U'), TypeVar('V'), TypeVar('W')
Color = Tuple[int, int, int]
Coordinate = Tuple[int, int]
Pair = Tuple[T, T]
Line = List[Coordinate]
Rectangle = Pair[Coordinate]
Matrix = Parametrizable[List[List[T]]]

# For more typing guidelines, see: /home/gabriel/dev/gbc/remote_first_project/graphics/tools/tests/graph_palettes/main.py


def image_to_points(img_fp: str) -> Dict[Color, List[Coordinate]]:
    """Opens an image and convert it to a list of point by color.
    Arguments:
        - img_fp: a string representing the filepath to the image
    Returns:
        A dictionary (mapping color -> list of points) containing every
        "color layer" represented as a list of coordinates with upper left
        corner as the (0, 0).
    """
    im = Image.open(img_fp)
    im = im.convert('RGB')
    im_width, im_height = im.size

    points_by_color = {}

    for x in range(0,im_width):
        for y in range(0,im_height):
            pos = (x, y)
            color = im.getpixel(pos)
            points_by_color[color] = points_by_color.get(color, []) + [pos]

    # Just to make sure that every coordinate appears only once
    for color in points_by_color.keys():
        points_by_color[color] = list(set(points_by_color[color]))

    return points_by_color


def points_to_rectangles(points: List[Coordinate]) -> List[Rectangle]:
    """Converts a list of points into a list of nonoverlapping rectangles.
    Arguments:
        - points: [(int, int)] representing coordinates in a XY points
    Returns:
        A list of rectangles that covers the inputted points
    """
    # Those are unitary vector in the coordinates planes so that we can
    # "walk" incrementally in a given direction
    directions = [
        (1, 0),
        (0, 1),
    ]

    # This basically does vector addition
    def step_in_direction(direction: Coordinate, point: Coordinate) -> Coordinate:
        return tuple(map(lambda i, j: i+j, direction, point))

    # These lines may have overlaps, so they have to be
    # culled later to "proper" lines
    possible_lines = []

    # For every point, pick every direction and see how far can we go with it
    for point in points:
        for direction in directions:
            line = []
            position = point

            # We have a point and a direction, now we try to go as far as
            # possible.
            while position in points:
                line.append(position)
                position = step_in_direction(direction, position)

            # We hit a wall and couldn't go further.
            # So this is the longest line in that direction start at that point.
            possible_lines.append(line)


    # Now, from all possible lines, we pick the longest non-overlapping lines.
    points_taken = set()
    actual_lines = []

    # Every non-overlapping line is as desirable as however long it is.
    # If that line overlaps with another line, we simply can't pick it.
    # if line is non-overlapping:
    #    Length(line) = len(line)
    # else:
    #    Length(line) = some really negative number to flag it
    Length = lambda line: sum([1 if point not in points_taken
                            else -2 * len(line)
                            for point in line])

    # If we still have lines left
    while len(possible_lines) > 0:
        # Pick the longest one
        possible_lines.sort(key=Length, reverse=True)
        line = possible_lines.pop(0)
        actual_lines.append(line)

        for point in line:
            points_taken |= set([point])

        # Remove any overlapping line that we could pick afterwards
        # (this will remove lines that could overlap with the line we just picked)
        possible_lines = [line for line in possible_lines if Length(line) > 0]



    # Once we have our lines, we put them in a "standard" notation:
    # leftmost-uppermost coordinate first, rightmost-lowest coordinate last
    rectangles: List[Rectangle] = [(sorted(line)[0], sorted(line)[-1])
                                   for line in actual_lines]
    del actual_lines
    del points
    del points_taken


    # Same algorithm as before:
    # 1. Generate all possible biggest rectangles
    # 2. Pick non-overlapping ones from the previous list
    possible_rectangles = []

    # This basically does an: IF coordinate_to_change THEN _to ELSE _from
    def translate(direction: Coordinate,
                   _from: Coordinate, _to: Coordinate) -> Coordinate:
        # Only changes the coordinate on the direction we are moving to
        return tuple(map(lambda _if, t, f: t if _if != 0 else f, direction, _from, _to))

    # This "projects" the coordinate unto an axis/direction.
    # Basically does point[0] or point[1] depending on the direction
    def pick_component(direction, point):
        return sum(map(lambda d_component, p_component: d_component * p_component,
                       direction, point))

    # def set_component(direction, point, value):
    #     index = list(direction).index(1)
    #     lpoint = list(point)
    #     lpoint[index] = value
    #     return tuple(lpoint)

    # (1, 0) if direction is (0, 1) else (0, 1)
    def inverse_direction(direction):
        return tuple(map(lambda c: 1 if c == 0 else 0, direction))

    def are_neighbours(direction, A: Rectangle, B: Rectangle) -> bool:
        # If they are mergeable neighbours, the start of A should
        # align with the start of B along direction !D and so should
        # their ends.
        other_direction = inverse_direction(direction)

        # Starts don't align along !D
        if pick_component(other_direction, A[0]) != pick_component(other_direction, B[0]):
            return False

        # Ends don't align along !D
        if pick_component(other_direction, A[1]) != pick_component(other_direction, B[1]):
            return False

        # Also, there shouldn't be any "gap" between the end of A and the start
        # of B, in other words Start of B = End of A + 1 along the direction D
        if pick_component(direction, B[0]) != (pick_component(direction, A[1]) + 1):
            return False
        return True

    cant_merge_more = False
    while cant_merge_more is False:
        found_any_merge = False

        # Pick up a rectangle to merge
        for index in range(0, len(rectangles)):
            rectangle = rectangles[index]

            # Pick it up, removing it from the list
            rectangles.remove(rectangle)

            direction = directions[0]
            skipped_merges = 0
            while skipped_merges < 3:
                while ((neighbours := [i for i in rectangles
                                         if are_neighbours(direction, rectangle, i)])
                       and len(neighbours) > 0):

                    # Given an direction, a rectangle can have only one
                    # (or less) neighbouring rectangles, so if it does has one
                    # then it has only one.
                    rect = neighbours.pop(0)
                    rectangle = (rectangle[0], rect[1])

                    # Remove the rect from the pool of rectangles
                    rectangles.remove(rect)

                    # We found at least one merge
                    found_any_merge = True

                    skipped_merges = 0
                    direction = inverse_direction(direction)

                # This line alone doesn't mean we can't merge anymore,
                # but if we hit it multiple times consecutively it means
                # we already merged everything we could.
                skipped_merges += 1
                direction = inverse_direction(direction)

            # Put that rectangle back into the list.
            # Where we place it depends if we merged everything we could
            # out of it, or it was untouched, because merging already invalidates
            # the index while not merging should preserve the index for proper
            # looping.
            if found_any_merge:
                rectangles.append(rectangle)
            else:
                rectangles.insert(index, rectangle)

            # Merging invalidates our indexing, we have to restart
            if found_any_merge:
                break

        if not found_any_merge:
            cant_merge_more = True

    rectangles.sort()
    return rectangles


def dump_rectangle_solution(color_id: Color, original_fp: str,
                            rectangles: List[Rectangle]) -> None:
    with Image.open(original_fp) as old_im:
        im = Image.new('RGB', old_im.size, (0, 0, 0))

    template_colors: List[Color] = [
        (33, 43, 94),
        (99, 111, 178),
        (173, 196, 255),
        (255, 255, 255),
        (255, 204, 215),
        (255, 127, 189),
        (135, 36, 80),
        (229, 45, 64),
        (239, 96, 74),
        (255, 216, 119),
        (0, 204, 139),
        (0, 90, 117),
        (81, 58, 232),
        (25, 186, 255),
        (119, 49, 165),
        (185, 124, 255),
    ]

    random.shuffle(template_colors)
    color_counter = 0

    def get_color() -> Color:
        """Produces a pseudorandom color"""
        nonlocal color_counter
        color = template_colors[color_counter % len(template_colors)]
        color_counter += 1
        return color

    draw = ImageDraw.Draw(im)

    for rectangle in sorted(rectangles):
        (sx, sy), (ex, ey) = rectangle
        draw.rectangle([sx, sy, ex, ey], fill=get_color())

    folder, filename = tuple(original_fp.rsplit('/', 1))
    basename = filename.rsplit('.', 1)[0]
    color_str = '__{}_{}_{}'.format(*color_id)

    savepath = folder + '/dumps/' + basename + color_str + '.png'
    im.save(savepath)

    return None


def do_image(img_fp: str,
             color_callbacks: Dict[Color, Tuple[str, str]],
             start_color: Color,
             move_callback: str):

    points: Dict[Color, List[Coordinate]] = image_to_points(img_fp)

    if len(points[start_color]) > 1:
        raise IndexError(f"There are too many ({str(len(points[start_color]))}) "
                         f"start_color {str(start_color)} on image '{img_fp}'")

    start_position = points[start_color][0]
    del points[start_color]

    if (c := set(points.keys())) > (v := set(color_callbacks.keys())):
        raise IndexError(f"We don't have callback for {str(v - c)}")

    current_position = start_position

    layers = {color: points_to_rectangles(points)
              for color, points in points.items()}

    for color, rectangles in layers.items():
        dump_rectangle_solution(color, img_fp, rectangles)

    def distance(p1: Coordinate, p2: Coordinate):
        p1x, p1y = p1
        p2x, p2y = p2
        return ((p1x - p2x) ** 2 + (p1y - p2y) ** 2) ** 0.5

    for color, rectangles in layers.items():
        start_draw_rectangle, draw_rectangle, _exit = color_callbacks[color]

        started_drawing = False

        while len(rectangles) > 0:
            rectangles.sort(key=lambda r: distance(current_position, r[0]))
            rectangle = rectangles.pop(0)

            current_position = move_callback(current_position, rectangle[0])

            if not started_drawing:
                current_position = start_draw_rectangle(current_position, rectangle)
                started_drawing = True
            else:
                current_position = draw_rectangle(current_position, rectangle)

            if current_position is None:
                raise IndexError(f"current_position was None'd when drawing "
                                 f"rectangle {str(rectangle)} at "
                                 f"{current_position}"
                                 f"{' while starting' if not started_drawing else ''}")

        # To exit from current color
        _exit(current_position)


def print_move(f: Coordinate, t: Coordinate) -> Coordinate:
    print(f"Moving from {f} to {t}")
    return t

def print_draw(p: Coordinate, r: Rectangle) -> Coordinate:
    print(f"Drawing at {p} rectangle {r}")
    return p

def print_start(p: Coordinate, r: Rectangle) -> Coordinate:
    print(f"Starting to draw at {p} rectangle {r}")
    return print_draw(p, r)

def print_exit(p: Coordinate) -> None:
    print(f"Exiting at {p}")

no_move = lambda f, t: t
no_start = no_move
no_draw = lambda p, r: p
no_exit = lambda p: None

# fp = '/home/gabriel/Downloads/LinuxLNP-0.44.12-r03/my-py-scripts/xonsh-scripts/example.png'
# example_img = image_to_points(fp)
# dump_rectangle_solution((0,255,0), fp, points_to_rectangles(example_img[(0,255,0)]))
