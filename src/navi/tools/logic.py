import math

__author__ = 'paoolo'

HALF_ROBO = 160.0

SOFT_LIMIT = 450.0
HARD_LIMIT = 200.0


def calculate(radius, linear_speed, angular_speed):
    if radius is None:
        left, right = linear_speed, linear_speed

    elif radius == 0:
        val = HALF_ROBO * math.tan(angular_speed)
        left, right = val + linear_speed, -val + linear_speed

    else:
        left = (radius + HALF_ROBO) * (linear_speed / radius)
        right = (radius - HALF_ROBO) * (linear_speed / radius)

    return left, right


def bound_speed(speed, distance):
    if distance < HARD_LIMIT:
        return 0
    elif HARD_LIMIT <= distance < SOFT_LIMIT:
        return (speed / (SOFT_LIMIT - HARD_LIMIT)) * distance - (speed * HARD_LIMIT) / (SOFT_LIMIT - HARD_LIMIT)
    else:
        return speed


ANGLE = 20


def get_linear_speed(left, right):
    linear_speed = (left + right) / 2.0
    return linear_speed


def get_radius(left, right, linear_speed=None):
    if linear_speed is None:
        linear_speed = get_linear_speed(left, right)
    diff = left - right
    if linear_speed == 0:
        radius = 0
    else:
        if diff == 0:
            radius = None
        else:
            radius = HALF_ROBO * (left + right) / diff
    return radius


def get_angular_speed(radius, left, right, linear_speed=None):
    if linear_speed is None:
        linear_speed = get_linear_speed(left, right)
    if radius is None:
        angular_speed = 0
    elif radius == 0:
        angular_speed = math.atan(left / HALF_ROBO)
    else:
        angular_speed = math.atan(linear_speed / radius)
    return angular_speed


DIV = 40


def change_angle(angle, left, right):
    if angle < 0:
        left = (-angle / DIV) * left
        right += (-angle / DIV) * right
    else:
        left += (angle / DIV) * left
        right = (angle / DIV) * right
    return left, right


def check_trajectory(scan, left, right):
    min_distance = None
    left_angle, right_angle = None, None

    linear_speed = get_linear_speed(left, right)

    if linear_speed > 0:
        for angle, distance in sorted(scan.items()):
            if angle <= -ANGLE:
                if distance == 0 or distance > SOFT_LIMIT * 2:
                    if left_angle is None or angle > left_angle:
                        left_angle = angle
            elif -ANGLE < angle < ANGLE:
                if distance > 10.0:
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
            elif ANGLE <= angle:
                if distance == 0 or distance > SOFT_LIMIT * 2:
                    if right_angle is None or angle < right_angle:
                        right_angle = angle

    if min_distance is not None:
        new_linear_speed = bound_speed(linear_speed, min_distance)
        left, right = map(lambda val: int((float(new_linear_speed) / linear_speed) * val), (left, right))

    new_angle = None
    if left_angle is not None and right_angle is not None:
        if -left_angle < right_angle:
            new_angle = left_angle
        else:
            new_angle = right_angle
    elif left_angle is not None and right_angle is None:
        new_angle = left_angle
    elif left_angle is None and right_angle is not None:
        new_angle = right_angle

    if new_angle is not None:
        left, right = change_angle(new_angle, left, right)
        print 'Turn to %d (%d, %d)' % (new_angle, left, right)

    return left, right


class Point():
    def __init__(self, x, y, fi):
        self.x, self.y, self.fi = x, y, fi


def get_phase_angle(target, r):
    return math.atan((target.y - r.y) / (target.x - r.x))


def detect_if_oscillatory_motion():
    pass


def get_point_for_scan(distance, angle):
    """
    For values (distance, angle) from scan compute relative coordinates of point.

    :param distance: number
    :param angle: number [rad]
    :return: tuple of two numbers (x, y)
    """
    return distance * math.sin(angle), distance * math.cos(angle)


def do_it(scan):
    for distance, angle in scan.items():
        pass
