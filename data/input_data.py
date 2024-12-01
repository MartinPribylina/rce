from .my_exceptions import AlreadyExists
from .point import Point

class InputData:
    def __init__(self, points = None):
        self.data = {}
        if points is None:
            return
        # Iterate over the data and create Point
        for point in points:
            x = float(point['x'])
            y = float(point['y'])
            point = Point(x, y, point['class_name'])  # Create Point
            self.add_point(point)  # Add the Point to InputData

    def add_point(self, point: Point) -> bool:
        """
        Adds a point to the InputData if it does not already exist.

        Args:
            point (Point): The Point to add to the InputData.

        Returns:
            bool: True if the point was added successfully, False if the point does not exist or
            if the point already exists in the InputData.

        Raises:
            AlreadyExists: If the point already exists in the InputData.
        """
        try:
            if self.contains_point(point):
                print("Point already exists")
                raise AlreadyExists
            self.data[point.key()] = point
            return True
        except ValueError:
            print("Invalid Point")
            return False
    
    def remove_point(self, point: Point) -> bool:
        """
        Removes a point from the InputData if it exists.

        Args:
            point (Point): The Point  to remove from the InputData.

        Returns:
            bool: True if the point was successfully removed, False if the point does not exist
            or if an invalid point is provided.

        Raises:
            Exception: If an invalid point is provided.
        """
        if self.contains_point(point):
            self.data.pop(point.key())
            return True

        return False
    
    def remove_all_points(self):
        """
        Removes all points from the InputData.
        """
        self.data.clear()

    def contains_point(self, point: Point) -> bool:
        """
        Checks if a point exists in the InputData.

        Args:
            point (Point): The Point to check for existence in the InputData.

        Returns:
            bool: True if the point exists in the InputData, False otherwise.
        """

        return point.key() in self.data