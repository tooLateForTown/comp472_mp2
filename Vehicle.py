class Vehicle:
    letter = '?'
    x = 0  # top-left position of first square
    y = 0  # top-left position of first square
    length = 0
    escaped = False
    gas = 100
    horizontal = False

    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        orientation = "horiz" if self.horizontal else "vert"
        top_left = chr(97+self.x) + str(self.y+1)
        return f"{self.letter}=[gas={self.gas} {top_left} {orientation}={self.length}]"

