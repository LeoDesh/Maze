import matplotlib.pyplot as plt


def get_maze(length: int, width: int):
    result = [[0 for _ in range(length)] for _ in range(width)]
    for i in range(width):
        result[i][0] = 1
    return result


def get_maze_text():
    maze = []
    with open("maze.txt", "r") as file:
        for line in file:
            line = line.rstrip()
            row = []
            for c in line:
                if c == " ":
                    row.append(1)  # spaces are 1s
                else:
                    row.append(0)  # walls are 0s
            maze.append(row)
    return maze


def generate_maze(length: int, width: int):
    pass


def main():
    maze = get_maze_text()
    # maze = [[1, 1, 0], [0, 0.5, 1], [1, 1, 0]]
    print(maze)
    plt.pcolormesh(maze)
    plt.show()


if __name__ == "__main__":
    main()
