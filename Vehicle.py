import globals

class Vehicle:
    letter = '?'
    x = 0  # top-left position of first square
    y = 0  # top-left position of first square
    length = 0
    escaped = False
    gas = globals.DEFAULT_GAS
    horizontal = False

    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        orientation = "horiz" if self.horizontal else "vert"
        top_left = chr(97+self.x) + str(self.y+1)
        return f"{self.letter}=[gas={self.gas} {top_left} {orientation}={self.length}]"

    def get_right(self):
        # returns right-most X position (zero based) of vehicle
        if self.horizontal:
            return self.x + self.length - 1
        else:
            return self.x

    def get_bottom(self):
        if not self.horizontal:
            return self.y + self.length - 1
        else:
            return self.y

    def is_on_exit_row(self):
        return self.y <= 2 and self.get_bottom() >= 2




