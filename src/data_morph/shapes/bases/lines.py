"""Base class for shapes that are composed of lines."""

from typing import Iterable, Union

from .shape import Shape


class Lines(Shape):
    """
    Class representing a shape consisting of one or more lines.

    Parameters
    ----------
    *lines : Iterable[Iterable[Iterable[Union[int, float]]]]
        An iterable of two (x, y) pairs representing the endpoints
        of a line.
    """

    def __init__(self, *lines) -> None:
        self.lines = lines

    def __repr__(self) -> str:
        return self._recursive_repr('lines')

    def distance(self, x: Union[int, float], y: Union[int, float]) -> float:
        """
        Calculate the minimum distance from the lines of this shape to a point (x, y).

        Parameters
        ----------
        x, y : int or float
            Coordinates of a point in 2D space.

        Returns
        -------
        float
            The minimum distance from the lines of this shape to the point (x, y).
        """
        return min(
            self._distance_point_to_line(point=(x, y), line=line) for line in self.lines
        )

    def _distance_point_to_line(
        self,
        point: Iterable[Union[int, float]],
        line: Iterable[Iterable[Union[int, float]]],
    ) -> float:
        """
        Calculate the minimum distance between a point and a line.

        Parameters
        ----------
        point : Iterable[Union[int, float]]
            Coordinates of a point in 2D space.
        line : Iterable[Iterable[Union[int, float]]]
            Coordinates of the endpoints of a line in 2D space.

        Returns
        -------
        float
            The minimum distance between the point and the line.

        Notes
        -----
        Implementation based on `this VBA code`_

        .. this VBA code: http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
        """
        start, end = line
        line_mag = self._euclidean_distance(start, end)

        if line_mag < 0.00000001:
            # Arbitrarily large value
            return 9999

        px, py = point
        x1, y1 = start
        x2, y2 = end

        u1 = ((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1))
        u = u1 / (line_mag * line_mag)

        if (u < 0.00001) or (u > 1):
            # closest point does not fall within the line segment, take the shorter
            # distance to an endpoint
            distance = max(
                self._euclidean_distance(point, start),
                self._euclidean_distance(point, end),
            )
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            distance = self._euclidean_distance(point, (ix, iy))

        return distance
