def is_inside(point, bounds):
    if len(bounds) == 2:
        assert(len(bounds[0]) == 2 and len(bounds[1]) == 2)
        bounds = (bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1])
    if point[0] < bounds[0]: 
        return False
    if point[0] > bounds[0] + bounds[2]: 
        return False
    if point[1] < bounds[1]:
        return False
    if point[1] > bounds[1] + bounds[3]:
        return False
    return True

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)

# From Rosetta Code: Bresenham's line algorithm
def line(x0, y0, x1, y1):
    _points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            _points.append((x, y))
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            _points.append((x, y))
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    _points.append((x, y))
    return _points
