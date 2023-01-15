from math import sqrt
from settings import *

##returns true if the given circle object and rectangle.rect are collided by at least a buffer amount
def circle_rect_collided(c, r, buffer):
    cx = c.pos.x
    cy = c.pos.y
    rx = r.x
    ry = r.y
    test_x = cx
    test_y = cy

    if (cx < rx):
        test_x = rx
    elif (cx > rx + r.width):
        test_x = rx + r.width

    if (cy < ry):
        test_y = ry
    elif (cy > ry + r.height):
        test_y = ry + r.height

    dist_x = cx - test_x
    dist_y = cy - test_y
    distance = sqrt(dist_x ** 2 + dist_y ** 2)
    if (distance <= (c.width / 2) + buffer):
        return True
    else:
        return False