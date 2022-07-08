from shapely.geometry import box, Polygon
from shapely.affinity import translate


def cut_normalize(cut):
    # Moves cut to origin
    return translate(cut, -cut.bounds[0], -cut.bounds[1])


def bfs(x_size, y_size, gap, initial_point, polygon):

    i_x = initial_point[0]
    i_y = initial_point[1]

    cuts = []

    queue = []
    visited = {}

    queue.append((i_x, i_y))

    while queue:

        x, y = queue.pop(0)

        if (x, y) in visited:
            continue

        visited[(x, y)] = True

        new_box = box(x, y, x + x_size, y + y_size)

        if polygon.intersects(new_box):
            cuts.append(cut_normalize(polygon.intersection(new_box)))

        if x + x_size + gap < polygon.bounds[2]:
            queue.append((x + x_size + gap, y))

        if y + y_size + gap < polygon.bounds[3]:
            queue.append((x, y + y_size + gap))

    return cuts


def main():
    # Example polygon
    xy = [[0, 0], [0, 4], [4, 4], [4, 0], [0, 0]]
    polygon_shape = Polygon(xy)

    cuts = bfs(0.5, 0.5, 0.01, (0, 0), polygon_shape)

    print("Cuts")

    for cut in cuts:
        print(list(cut.exterior.coords))


if __name__ == "__main__":
    main()
