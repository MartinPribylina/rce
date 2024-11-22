from .my_exceptions import AlreadyExists
from .point import Point

class InputData:
    def __init__(self, data: str = None):
        self.data = {}
        if data is None:
            return
        # Iterate over the data and create Point objects
        for key, value in data['data'].items():
            x = float(value['x'])
            y = float(value['y'])
            point = Point(x, y, value['class_name'])  # Create Point object
            self.add_point(point)  # Add the Point to InputData

    def add_point(self, point: Point) -> bool:
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
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            if self.contains_point(point):
                self.data.pop(point.key())
                return True
            print("Remove Point: Point does not exist")
        except ValueError:
            print("Remove Point: Invalid Point")
        return False

    def contains_point(self, point: Point) -> bool:
        return point.key() in self.data