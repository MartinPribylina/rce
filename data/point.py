class Point:
    def __init__(self, x, y, class_name):
        self.x = x
        self.y = y
        self.class_name = class_name

    def get_color(self):
        return self.class_name
    
    def key(self):
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