class Point:
    def __init__(self, x, y, class_name):
        self.x = x
        self.y = y
        self.class_name = class_name

    def get_color(self):
        colors = {"Red": "red", "Green": "green", "Blue": "blue"}
        return colors.get(self.class_name, "black")
    
    def key(self):
        return f"{self.x},{self.y}"