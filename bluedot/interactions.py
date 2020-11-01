from time import time
from math import atan2, degrees, hypot

class BlueDotPosition:
    """
    Represents a position of where the blue dot is pressed, released or held.

    :param float x:
        The x position of the Blue Dot, 0 being centre, -1 being far left
        and 1 being far right.

    :param float y:
        The y position of the Blue Dot, 0 being centre, -1 being at the
        bottom and 1 being at the top.
    """
    def __init__(self, col, row, x, y):
        self._time = time()
        self._col = int(col)
        self._row = int(row)
        self._x = self._clamped(float(x))
        self._y = self._clamped(float(y))
        self._angle = None
        self._distance = None

    def _clamped(self, v):
        return max(-1, min(1, v))

    @property
    def col(self):
        """
        The column.
        """
        return self._col

    @property
    def row(self):
        """
        The row.
        """
        return self._row

    @property
    def x(self):
        """
        The x position of the Blue Dot, 0 being centre, -1 being far
        left and 1 being far right.
        """
        return self._x

    @property
    def y(self):
        """
        The y position of the Blue Dot, 0 being centre, -1 being at
        the bottom and 1 being at the top.
        """
        return self._y

    @property
    def angle(self):
        """
        The angle from centre of where the Blue Dot is pressed, held or released.
        0 degrees is up, 0..180 degrees clockwise, -180..0 degrees anti-clockwise.
        """
        if self._angle is None:
            self._angle = degrees(atan2(self.x, self.y))
        return self._angle

    @property
    def distance(self):
        """
        The distance from centre of where the Blue Dot is pressed, held or released.
        The radius of the Blue Dot is 1.
        """
        if self._distance is None:
            self._distance = self._clamped(hypot(self.x, self.y))
        return self._distance

    @property
    def middle(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released in the middle.
        """
        return self.distance <= 0.5

    @property
    def top(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released at the top.
        """
        return self.distance > 0.5 and (-45 < self.angle <= 45)

    @property
    def right(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released on the right.
        """
        return self.distance > 0.5 and (45 < self.angle <= 135)

    @property
    def bottom(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released at the bottom.
        """
        return self.distance > 0.5 and (self.angle > 135 or self.angle <= -135)

    @property
    def left(self):
        """
        Returns ``True`` if the Blue Dot is pressed, held or released on the left.
        """
        return self.distance > 0.5 and (-135 < self.angle <= -45)

    @property
    def time(self):
        """
        The time the blue dot was at this position.

        .. note::

            This is the time the message was received from the Blue Dot app,
            not the time it was sent.
        """
        return self._time

    def __str__(self):
        return "BlueDotPosition - col={}, row={}, x={}, y={}".format(
            self.col, self.row, self.x, self.y
        )


class BlueDotInteraction:
    """
    Represents an interaction with the Blue Dot, from when it was pressed to
    when it was released.

    A :class:`BlueDotInteraction` can be active or inactive, i.e. it is active
    because the Blue Dot has not been released, or inactive because the Blue
    Dot was released and the interaction finished.

    :param BlueDotPosition pressed_position:
        The BlueDotPosition when the Blue Dot was pressed.
    """
    def __init__(self, pressed_position):
        self._active = True
        self._positions = []
        self._positions.append(pressed_position)

    @property
    def active(self):
        """
        Returns ``True`` if the interaction is still active, i.e. the Blue Dot
        hasnt been released.
        """
        return self._active

    @property
    def positions(self):
        """
        A sequence of :class:`BlueDotPosition` instances for all the positions
        which make up this interaction.

        The first position is where the Blue Dot was pressed, the last is where
        the Blue Dot was released, all position in between are where the position
        Blue Dot changed (i.e. moved) when it was held down.
        """
        return self._positions

    @property
    def pressed_position(self):
        """
        Returns the position when the Blue Dot was pressed i.e. where the
        interaction started.
        """
        return self._positions[0]

    @property
    def released_position(self):
        """
        Returns the position when the Blue Dot was released i.e. where the
        interaction ended.

        If the interaction is still active it returns ``None``.
        """
        return self._positions[-1] if not self.active else None

    @property
    def current_position(self):
        """
        Returns the current position for the interaction.

        If the interaction is inactive, it will return the position when the
        Blue Dot was released.
        """
        return self._positions[-1]

    @property
    def previous_position(self):
        """
        Returns the previous position for the interaction.

        If the interaction contains only 1 position, None will be returned.
        """
        return self._positions[-2] if len(self._positions) > 1 else None

    @property
    def duration(self):
        """
        Returns the duration in seconds of the interaction, i.e. the amount time
        between when the Blue Dot was pressed and now or when it was released.
        """
        if self.active:
            return time() - self.pressed_position.time
        else:
            return self.released_position.time - self.pressed_position.time

    @property
    def distance(self):
        """
        Returns the total distance of the Blue Dot interaction
        """
        dist = 0
        for i in range(1, len(self._positions)):
            p1 = self._positions[i-1]
            p2 = self._positions[i]
            dist += hypot(p2.x - p1.x, p2.y - p1.y)

        return dist

    def moved(self, moved_position):
        """
        Adds an additional position to the interaction, called when the position
        the Blue Dot is pressed moves.
        """
        if self._active:
            self._positions.append(moved_position)

    def released(self, released_position):
        """
        Called when the Blue Dot is released and completes a Blue Dot interaction

        :param BlueDotPosition released_position:
            The BlueDotPosition when the Blue Dot was released.
        """
        self._active = False
        self._positions.append(released_position)


class BlueDotSwipe:
    """
    Represents a Blue Dot swipe interaction.

    A :class:`BlueDotSwipe` can be valid or invalid based on whether the Blue Dot
    interaction was a swipe or not.

    :param BlueDotInteraction interaction:
        The BlueDotInteraction object to be used to determine whether the interaction
        was a swipe.
    """
    def __init__(self, interaction):
        self._interaction = interaction
        self._col = interaction.current_position.col
        self._col = interaction.current_position.col
        self._speed_threshold = 2
        self._angle = None
        self._distance = None
        self._valid = self._is_valid_swipe()

    def _is_valid_swipe(self):
        #the validity of a swipe is based on the speed of the interaction,
        # so a short fast swipe is valid as well as a long slow swipe
        #self._speed = self.distance / self.interaction.duration
        self._speed = self.distance / self.interaction.duration
        if not self.interaction.active and self._speed > self._speed_threshold:
            return True
        else:
            return False

    @property
    def col(self):
        """
        The column.
        """
        return self.interaction.current_position.col

    @property
    def row(self):
        """
        The row.
        """
        return self.interaction.current_position.row

    @property
    def interaction(self):
        """
        The :class:`BlueDotInteraction` object relating to this swipe.
        """
        return self._interaction

    @property
    def valid(self):
        """
        Returns ``True`` if the Blue Dot interaction is a swipe.
        """
        return self._valid

    @property
    def distance(self):
        """
        Returns the distance of the swipe (i.e. the distance between the pressed
        and released positions)
        """
        # should this be the total length of the swipe. All the points? It might be slow to calculate
        if self._distance == None:
            self._distance = hypot(
                self.interaction.released_position.x - self.interaction.pressed_position.x,
                self.interaction.released_position.y - self.interaction.pressed_position.y)

        return self._distance

    @property
    def angle(self):
        """
        Returns the angle of the swipe (i.e. the angle between the pressed
        and released positions)
        """
        if self._angle == None:
            self._angle = degrees(atan2(
                self.interaction.released_position.x - self.interaction.pressed_position.x,
                self.interaction.released_position.y - self.interaction.pressed_position.y))

        return self._angle

    @property
    def speed(self):
        """
        Returns the speed of the swipe in Blue Dot radius / second.
        """
        return self._speed

    @property
    def up(self):
        """
        Returns ``True`` if the Blue Dot was swiped up.
        """
        return self.valid and (-45 < self.angle <= 45)

    @property
    def down(self):
        """
        Returns ``True`` if the Blue Dot was swiped down.
        """
        return self.valid and (self.angle > 135 or self.angle <= -135)

    @property
    def left(self):
        """
        Returns ``True`` if the Blue Dot was swiped left.
        """
        return self.valid and (-135 < self.angle <= -45)

    @property
    def right(self):
        """
        Returns ``True`` if the Blue Dot was swiped right.
        """
        return self.valid and (45 < self.angle <= 135)

    @property
    def direction(self):
        """
        Returns the direction ("up", "down", "left", "right") of the swipe.
        If the swipe is not valid `None` is returned. 
        """
        if self.up:
            return "up"
        elif self.down:
            return "down"
        elif self.right:
            return "right"
        elif self.left:
            return "left"
        else:
            return None

    def __str__(self):
        return "BlueDotSwipe - col={}, row={}, direction={}".format(
            self.col, self.row, self.direction
        )


class BlueDotRotation:
    def __init__(self, interaction, no_of_segments):
        """
        Represents a Blue Dot rotation.

        A :class:`BlueDotRotation` can be valid or invalid based on whether the Blue Dot
        interaction was a rotation or not.

        :param BlueDotInteraction interaction:
            The object to be used to determine whether the interaction
            was a rotation.
        """
        self._interaction = interaction
        self._value = 0
        self._clockwise = False
        self._anti_clockwise = False
        self._previous_segment = 0
        self._current_segment = 0

        prev_pos = interaction.previous_position
        pos = interaction.current_position

        # was there a previous position (i.e. the interaction has more than 2 positions)
        if prev_pos != None:

            # were both positions in the 'outer circle'
            if prev_pos.distance > 0.5 and pos.distance > 0.5:

                # what segments are the positions in
                deg_per_seg = (360 / no_of_segments)
                self._previous_segment = int((prev_pos.angle + 180) / deg_per_seg) + 1
                self._current_segment = int((pos.angle + 180) / deg_per_seg) + 1

                # were the positions in different segments
                if self._previous_segment != self._current_segment:
                    # calculate the rotation
                    diff = self._previous_segment - self._current_segment
                    if diff != 0:
                        if diff == -1:
                            self._value = 1
                        elif diff == 1:
                            self._value = -1
                        elif diff == (no_of_segments - 1):
                            self._value = 1
                        elif diff == (1 - no_of_segments):
                            self._value = -1

    @property
    def col(self):
        """
        The column.
        """
        return self.interaction.current_position.col

    @property
    def row(self):
        """
        The row.
        """
        return self.interaction.current_position.row

    @property
    def valid(self):
        """
        Returns ``True`` if the Blue Dot was rotated.
        """
        return self._value != 0

    @property
    def interaction(self):
        """
        The :class:`BlueDotInteraction` object relating to this rotation.
        """
        return self._interaction

    @property
    def value(self):
        """
        Returns 0 if the Blue Dot wasn't rotated, -1 if rotated anti-clockwise and 1 if rotated clockwise.
        """
        return self._value

    @property
    def anti_clockwise(self):
        """
        Returns ``True`` if the Blue Dot was rotated anti-clockwise.
        """
        return self._value == -1

    @property
    def clockwise(self):
        """
        Returns ``True`` if the Blue Dot was rotated clockwise.
        """
        return self._value == 1

    def __str__(self):
        return "BlueDotRotation - col={}, row={}, value={}".format(
            self.col, self.row, self.value
        )
