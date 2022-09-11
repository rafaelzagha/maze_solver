from time import sleep
import cv2 as cv
from threading import Thread


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
        return 0 <= self.x < width and 0 <= self.y < height

    def children(self):
        dir4 = [Point(0, -1), Point(0, 1), Point(1, 0), Point(-1, 0)]
        adj = []
        for d in dir4:
            adj.append(self + d)
        return adj


def solve(s: Point, e: Point):
    global h, w, img, px
    found = False
    q = []  # queue for children points
    v = [[0 for _ in range(w)] for _ in range(h)]  # visited points: o for not visited, 1 for visited
    parentmap = [[Point() for _ in range(w)] for _ in range(h)]  # parent map for retracing the shortest path

    q.append(s)

    while len(q) > 0:
        parent = q.pop(0)
        for cell in parent.children():
            if cell.in_bounds(h, w) and v[cell.y][cell.x] == 0 and (list(img[cell.y][cell.x]) != [0, 0, 0]):
                q.append(cell)
                v[cell.y][cell.x] = 1
                parentmap[cell.y][cell.x] = parent
                img[cell.y][cell.x] = [255, 0, 0]
                if cell == e:
                    found = True
                    del q[:]
                    break
    path = []
    if found:
        point = e
        while point != s:
            path.append(point)
            point = parentmap[point.y][point.x]
        path.append(point)
        path.reverse()
        for i in range(1, len(path)):
            x1, y1 = path[i].x, path[i].y
            x2, y2 = path[i - 1].x, path[i - 1].y
            cv.line(img, (x2, y2), (x1, y1), (0, 255, 0), px)

        print("Path Found")
    else:
        print("Path Not Found")
    cv.imwrite('img.png', img)


def mouse_event(event, x, y, flags, params):
    global start, end, p, img, radius

    if event == cv.EVENT_LBUTTONUP:
        if p == 0:
            cv.ellipse(img, (x, y), (radius, radius), 0., 0., 360, (0, 0, 255), -1)
            start = Point(x, y)
            print("start = ", start)
            p += 1
        elif p == 1:
            cv.ellipse(img, (x, y), (radius, radius), 0., 0., 360, (0, 255, 0), -1)
            end = Point(x, y)
            print("end = ", end)
            p += 1


def display():
    global img
    cv.imshow('Maze', img)
    cv.setMouseCallback('Maze', mouse_event)
    while True:
        cv.imshow('Maze', img)
        cv.waitKey(15)


px = 3  # thickness of answer line in pixels
radius = 5  # radius of start and end points
p = 0  # how many points were added
start = Point()
end = Point()

img = cv.imread('mazes/maze.png', cv.IMREAD_GRAYSCALE)
ret, img = cv.threshold(img, 150, 255, cv.THRESH_BINARY)
img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
# img = cv.resize(img, (0, 0), fx=0.2, fy=0.2)
h, w = img.shape[:2]

t = Thread(target=display, daemon=True)
t.start()

print('Enter start and end points')

while p < 2:
    pass

solve(start, end)
cv.waitKey(1000)
