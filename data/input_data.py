from .my_exceptions import AlreadyExists
from .point import Point

class InputData:
    def __init__(self, points = None):
        self.data = {}
        if points is None:
            return
        # Iterate over the data and create Point objects
        for point in points:
            x = float(point['x'])
            y = float(point['y'])
            point = Point(x, y, point['class_name'])  # Create Point object
            self.add_point(point)  # Add the Point to InputData

    def add_point(self, point: Point) -> bool:
        """
        Adds a point to the InputData object if it does not already exist.

        Args:
            point (Point): The Point object to add to the InputData object.

        Returns:
            bool: True if the point was added successfully, False if the point does not exist or
            if the point already exists in the InputData object.

        Raises:
            AlreadyExists: If the point already exists in the InputData object.
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
        Removes a point from the InputData object if it exists.

        Args:
            point (Point): The Point object to remove from the InputData object.

        Returns:
            bool: True if the point was successfully removed, False if the point does not exist
            or if an invalid point is provided.

        Raises:
            Exception: If an invalid point is provided.
        """
        try:
            if self.contains_point(point):
                self.data.pop(point.key())
                return True
            print("Remove Point: Point does not exist")
        except Exception:
            print("Remove Point: Invalid Point")

        return False

    def contains_point(self, point: Point) -> bool:
        """
        Checks if a point exists in the InputData object.

        Args:
            point (Point): The Point object to check for existence in the InputData object.

        Returns:
            bool: True if the point exists in the InputData object, False otherwise.
        """

        return point.key() in self.data