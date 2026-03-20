import matplotlib.pyplot as plt

key_dict = {
    "|": [["y", -1], ["y", 1]],
    "-": [["x", -1], ["x", 1]],
    "L": [["y", -1], ["x", 1]],
    "J": [["y", -1], ["x", -1]],
    "7": [["x", -1], ["y", 1]],
    "F": [["x", 1], ["y", 1]],
}

start = "S"


def calc_coord(coords, axis, action):
    act_coord = coords[axis] + action
    if act_coord >= 0:
        if axis == "y":
            return (coords["x"], act_coord)
        else:
            return (act_coord, coords["y"])
    else:
        return "."


def get_coords(coords, instructions):
    connect_coords = []
    for inst in instructions:
        axis, action = inst
        if c_coord := calc_coord(coords, axis, action):
            connect_coords.append(c_coord)
        else:
            return "."
    return connect_coords


def print_rows(rows):
    for row in rows:
        print(row)


def draw_path(path):
    x_c, y_c = zip(*path)
    plt.plot(x_c, y_c, marker='o', color='b', linestyle='-')
    plt.gca().invert_yaxis()
    plt.xlim(-1, 5)
    plt.ylim(5, -1)
    plt.xticks(range(5))
    plt.yticks(range(5))
    plt.grid(True)
    plt.show()


def find_path(field, s_coords, locked_pipes):
    path = []
    s_x, s_y = s_coords
    current_coords = (s_x, s_y)

    def check_vars(next_vars, is_first):
        for var in next_vars:
            if var not in locked_pipes:
                pipes = field[var[1]][var[0]]
                if pipes != "." and (is_first or pipes != "S") and current_coords in pipes and var not in path:
                    return var

    def gen_start_vars():
        yield (s_x + 1, s_y)
        yield (s_x - 1, s_y)
        yield (s_x, s_y + 1)
        yield (s_x, s_y - 1)


    is_first = True
    while True:
        if is_first:
            next = check_vars(((var[0], var[1]) for var in gen_start_vars() if var[0] >=0 and var[1] >= 0), True)
        else:
            next = check_vars(field[current_coords[1]][current_coords[0]], False)
        if next == s_coords or next is None:
            return path
        else:
            path.append(next)
            current_coords = next
            is_first = False


def analysis(field):
    result_field = []
    s_coords = None
    for y, row in enumerate(field):
        result_row = []
        for x, char in enumerate(row):
            if char == start:
                s_coords = (x, y)
                result_row.append(start)
            elif char in key_dict:
                result_row.append(get_coords({"x":x, "y": y}, key_dict.get(char)))
            else:
                result_row.append(".")
        result_field.append(result_row)

    print_rows(result_field)
    locked_pipes = set()
    paths = []
    while True:
        path = find_path(result_field, s_coords, locked_pipes)
        if not path:
            break
        paths.append(path)
        locked_pipes.update(path)
    max_path = max(paths, key=len)
    print(f"max path - {max_path}")
    draw_path(max_path)


#    0   1   2   3   4
# 0[".",".",".",".","."],
# 1[".","S","-","7","."],
# 2[".","|",".","|","."],
# 3[".","L","-","J","."],
# 4[".",".",".",".","."]


test1 = [
    [".",".",".",".","."],
    [".","S","-","7","."],
    [".","|",".","|","."],
    [".","L","-","J","."],
    [".",".",".",".","."]
]


analysis(test1)


#    0   1   2   3   4
#0 [".",".","F","7","."],
#1 [".","F","J","|","."],
#2 ["S","J",".","L","7"],
#3 ["|","F","-","-","J"],
#4 ["L","J",".",".","."]


test2 = [
    [".",".","F","7","."],
    [".","F","J","|","."],
    ["S","J",".","L","7"],
    ["|","F","-","-","J"],
    ["L","J",".",".","."]
]


analysis(test2)


test3 = [
    ["7","-","F","7","-"],
    [".","F","J","|","7"],
    ["S","J","L","L","7"],
    ["|","F","-","-","J"],
    ["L","J",".","L","J"]
]


analysis(test3)

