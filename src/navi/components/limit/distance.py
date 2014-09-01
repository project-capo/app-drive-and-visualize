from navi.tools import logic
from navi.components.component import Component

__author__ = 'paoolo'


class Distance(Component):
    """
    Used to control speed.
    """

    def __init__(self, hokuyo):
        super(Distance, self).__init__()
        hokuyo.subscribe(self)

        self._scan = None

        self._alpha = 0.6
        self._max_speed = 700.0
        self._robo_width = 450.0
        self._hard_limit = 250.0
        self._soft_limit = 500.0
        self._scaner_dist_offset = 10.0
        self._angle_range = 24.0

    def handle(self, scan):
        self._scan = scan

    def modify(self, left, right):
        if left > 0 or right > 0:
            current_angle = logic.get_angle(left, right, self._robo_width)
            current_speed = logic.get_speed(left, right)

            scan = self._scan

            if scan is not None:
                min_distance, _ = logic.get_min_distance(scan, current_angle,
                                                         self._scaner_dist_offset, self._angle_range)
                if min_distance is not None:

                    soft_limit = logic.get_soft_limit(current_speed, self._max_speed,
                                                      self._soft_limit, self._hard_limit, self._alpha)

                    if self._hard_limit < min_distance < soft_limit:
                        max_speed = logic.get_max_speed(min_distance, soft_limit, self._hard_limit, self._max_speed)
                        if current_speed > max_speed:
                            left, right = self._calculate_new_left_right(left, right, max_speed, current_speed)

                    elif min_distance <= self._hard_limit:
                        left, right = 0, 0

            else:
                left, right = 0.0, 0.0

        return left, right

    @staticmethod
    def _calculate_new_left_right(left, right, max_speed, current_speed):
        if current_speed > 0:
            divide = max_speed / current_speed
            return left * divide, right * divide
        else:
            return left, right

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, val):
        self._alpha = float(val)

    @property
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self, val):
        self._max_speed = float(val)

    @property
    def robo_width(self):
        return self._robo_width

    @robo_width.setter
    def robo_width(self, val):
        self._robo_width = float(val)

    @property
    def hard_limit(self):
        return self._hard_limit

    @hard_limit.setter
    def hard_limit(self, val):
        self._hard_limit = float(val)

    @property
    def soft_limit(self):
        return self._soft_limit

    @soft_limit.setter
    def soft_limit(self, val):
        self._soft_limit = float(val)