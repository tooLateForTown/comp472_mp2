class Vehicle:
    letter = '?'
    x = 0
    y = 0
    length = 0
    escaped = False
    gas = 100

    def __init__(self, letter):
        self.letter = letter

    def __str__(self):
        return f"{self.letter}({self.gas})"
