from PIL import Image, ImageDraw


class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def in_bounds(self, height, width):
        return 0 <= self.x < height and 0 <= self.y < width

    def children(self):
        dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
        adj = []
        for d in dir4:
            adj.append(self + d)
        return adj


def bfs(maze, start: Point, end: Point):  # maze has to be rectangle
    found = False
    queue = []
    visited = []
    parentmap = [[Point() for _ in range(len(maze[i]))] for i in range(len(maze))]

    queue.append(start)
    display(maze, visited)
    visited.append(start)
    display(maze, visited)
    while len(queue) > 0:
        parent = queue.pop(0)
        for cell in parent.children():
            if cell.in_bounds(len(maze), len(maze[0])) and cell not in visited and maze[cell.x][cell.y] == 0:
                queue.append(cell)
                visited.append(cell)
                parentmap[cell.x][cell.y] = parent
                display(maze, visited)
                if cell == end:
                    found = True
                    del queue[:]
                    break


    path = []
    if found:
        point = end
        while point != start:
            path.append(point)
            point = parentmap[point.x][point.y]
            display(maze, visited, path)
        path.append(point)
        path.reverse()
        print("Path Found")
    else:
        print("Path Not Found")

    images[0].save('bfs-maze-gif.gif',
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=1, loop=0)


def dfs(maze, start:Point, end:Point):
    found = False
    visited = []
    stack = [start]
    parentmap = [[Point() for _ in range(len(maze[i]))] for i in range(len(maze))]
    while len(stack) > 0:
        current = stack.pop()
        if current == end:
            found = True
            break
        visited.append(current)
        display(maze, visited)
        for adj in current.children():
            if adj not in visited and adj.in_bounds(len(maze), len(maze[0])) and maze[adj.x][adj.y] == 0:
                parentmap[adj.x][adj.y] = current
                stack.append(adj)

    path = []
    if found:
        point = end
        while point != start:
            path.append(point)
            point = parentmap[point.x][point.y]
            display(maze, visited, path)
        path.append(point)
        path.reverse()
        print("Path Found")
    else:
        print("Path Not Found")

    images[0].save('dfs-maze-gif.gif',
                   save_all=True, append_images=images[1:],
                   optimize=False, duration=1, loop=0)


def display(maze, visited, the_path=None):
    the_path = [] if the_path is None else the_path
    im = Image.new('RGB', (zoom * len(maze[0]), zoom * len(maze)), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            color = (255, 255, 255)
            r = 0  # apply borders or not
            if maze[i][j] == 1:
                color = (0, 0, 0)
            if (i, j) == (start.x, start.y) or (i, j) == (end.x, end.y):
                color = (0, 255, 0)
                r = borders
            draw.rectangle((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1), fill=color)
            if Point(i, j) in visited:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                             fill=(255, 0, 0))
    for u in range(len(the_path) - 1):
        y = the_path[u].x * zoom + int(zoom / 2)
        x = the_path[u].y * zoom + int(zoom / 2)
        y1 = the_path[u + 1].x * zoom + int(zoom / 2)
        x1 = the_path[u + 1].y * zoom + int(zoom / 2)
        draw.line((x, y, x1, y1), fill=(0, 0, 255), width=5)
    draw.rectangle((0, 0, zoom * len(maze[0]), zoom * len(maze)), outline=(0, 255, 0), width=2)
    images.append(im)


maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

start = Point(1, 1)
end = Point(5, 19)

maze2 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

start2 = Point(1, 1)
end2 = Point(3, 7)

images = []
zoom = 30  # size of each tile in maze
borders = 6

dfs(maze, start, end)
del images
images = []
bfs(maze, start, end)
