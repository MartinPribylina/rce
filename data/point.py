class Point:
    def __init__(self, x, y, class_name):
        """
        Initializes a Point object with given coordinates and class name.

        :param x: int or float, x-coordinate of the point.
        :param y: int or float, y-coordinate of the point.
        :param class_name: str, class name of the point.
        """
        self.x = x
        self.y = y
        self.class_name = class_name

    def get_color(self):
        """
        Returns the color of the point - currently class_name = color

        :return: str, color of the point.
        """
        return self.class_name
    
    def key(self):
        """
        Returns a unique string key for the point. The key is a comma-separated value of the x and y coordinates.
        :return: str, unique string key for the point.
        """
        return f"{self.x},{self.y}"
    
    def __str__(self):
        str = "[{}, {}, class = {}]".format(self.x, self.y, self.class_name)
        return str
    
    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "class_name": self.class_name
        }