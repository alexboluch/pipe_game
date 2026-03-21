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


def draw_path(path, max_len):
    x_c, y_c = zip(*path)
    plt.plot(x_c, y_c, marker='o', color='b', linestyle='-')
    plt.gca().invert_yaxis()
    plt.xlim(-1, max_len)
    plt.ylim(max_len, -1)
    plt.xticks(range(max_len))
    plt.yticks(range(max_len))
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

    # print_rows(result_field)
    locked_pipes = set()
    paths = []
    while True:
        path = find_path(result_field, s_coords, locked_pipes)
        if not path:
            break
        paths.append(path)
        locked_pipes.update(path)
    max_path = max(paths, key=len)
    # print(f"max path - {max_path}")
    print(f"max count - {int((len(max_path) + 1) / 2)}")
    draw_path(max_path, len(field))
    return [s_coords,] + max_path


def open_file():
    field = []
    with open("puzzle_input.txt", "r", encoding="utf-8") as f:
        for line in f:
            row = list(line.strip())
            field.append(row)
    return field


path = analysis(open_file())


def analysis_path(path):
    path_len = len(path)
    total_sum = 0
    for i in range(path_len):
        x1, y1 = path[i]
        x2, y2 = path[(i + 1) % path_len]
        total_sum += (x1 * y2) - (x2 * y1)
    area = abs(total_sum) / 2
    print(f'nests count - {int(area - (path_len / 2) + 1)}')


analysis_path(path)