import numpy as np

import globals
from globals import DIRECTION
from Vehicle import Vehicle
from Move import Move


class BoardState:
    valid = False

    def __init__(self, config):
        self.vehicles = []
        self.board = np.full((6, 6), '.')
        self.valid = self.load_game(config)

    def load_game(self, config) -> bool:
        config = config.strip()
        if len(config) < 36:
            print("Setup needs to be at least 36 characters")
            return False
        # load Board array
        for row in range(0, 6):
            for col in range(0, 6):
                self.board[row][col] = config[row * 6 + col]
        # identify the vehicles
        for row in range(0, 6):
            for col in range(0, 6):
                letter = self.board[row][col]
                if letter != '.':
                    vehicle = self.get_vehicle(letter)
                    if vehicle is None:
                        v = Vehicle(letter)
                        v.x = col  # top left posit
                        v.y = row
                        # determine length and direction
                        if row < 5 and self.board[row + 1][col] == letter:
                            v.horizontal = False
                            temp_y = row
                            while temp_y <= 5 and self.board[temp_y][col] == letter:
                                v.length += 1
                                temp_y += 1
                        elif col < 5 and self.board[row][col + 1] == letter:
                            v.horizontal = True
                            temp_x = col
                            while temp_x <= 5 and self.board[row][temp_x] == letter:
                                v.length += 1
                                temp_x += 1
                        else:
                            print("Cannot determine orientation of " + letter)
                            return False

                        self.vehicles.append(v)
                    self.vehicles.sort(key=BoardState.letter_val)
        # load gas
        if len(config) > 36:
            for gas in config[36:].split(' '):
                if len(gas) > 1:
                    v = self.get_vehicle(gas[0])
                    if v is None:
                        print("Gas setup referring to vehicle not previously found.")
                        return False
                    print(f"Gas found for {v.letter}")
                    v.gas = int(gas[1:])
        return True

    def is_goal(self):
        return self.vehicle_at_exit('A')

    def vehicle_at_exit(self, letter):
        v = self.get_vehicle(letter)
        return (v.horizontal and v.get_right() >= 5) or (not v.horizontal and v.x == 5 and
                                                         v.y <= 2 and v.get_bottom() >= 2)

    def get_vehicle(self, letter) -> Vehicle:
        for v in self.vehicles:
            if v.letter == letter:
                return v
        return None

    def show_board(self):
        print('   a b c d e f')
        print("  -------------")
        count = 1
        for row in self.board:
            print(count, end='| ')
            count += 1
            for col in row:
                print(col, end=' ')
            print()
        print("  -------------")
        print(f"{len(self.vehicles)} vehicles: ", end='')
        for v in self.vehicles:
            print(v, end=' ')
        print()

    def board_config(self):
        s = ""
        for row in self.board:
            for col in row:
                s += col
        # gas values
        for v in self.vehicles:
            if v.gas != globals.DEFAULT_GAS:
                s += f" {v.letter}{v.gas}"
        return s

    @staticmethod
    def letter_val(vehicle):
        return ord(vehicle.letter)

    def number_free_spaces(self, x, y, direction) -> int:
        # doesn't count starting position
        count = 0
        if x < 0 or x > 5 or y < 0 or y > 5:
            return 0

        if direction == DIRECTION.UP:
            y -= 1
            while y >= 0 and self.board[y][x] == '.':
                count += 1
                y -= 1
        if direction == DIRECTION.DOWN:
            y += 1
            while y <= 5 and self.board[y][x] == '.':
                count += 1
                y += 1
        if direction == DIRECTION.RIGHT:
            x += 1
            while x <= 5 and self.board[y][x] == '.':
                count += 1
                x += 1
        if direction == DIRECTION.LEFT:
            x -= 1
            while x >= 0 and self.board[y][x] == '.':
                count += 1
                x -= 1

        return count

    def get_all_moves(self):
        moves = []
        print("Searching for all valid moves....")
        for v in self.vehicles:
            if v.horizontal:
                for i in range(0, self.number_free_spaces(v.x + v.length - 1, v.y, DIRECTION.RIGHT)):
                    m = Move(self, v, DIRECTION.RIGHT, i + 1)
                    moves.append(m)
                    # print(m)
                for i in range(0, self.number_free_spaces(v.x, v.y, DIRECTION.LEFT)):
                    m = Move(self, v, DIRECTION.LEFT, i + 1)
                    moves.append(m)
                    # print(m)
            if not v.horizontal:
                for i in range(0, self.number_free_spaces(v.x, v.y, DIRECTION.UP)):
                    m = Move(self, v, DIRECTION.UP, i + 1)
                    moves.append(m)
                    # print(m)
                for i in range(0, self.number_free_spaces(v.x, v.y + v.length - 1, DIRECTION.DOWN)):
                    m = Move(self, v, DIRECTION.DOWN, i + 1)
                    moves.append(m)
                    # print(m)
        return moves

    def rebuild_board_based_on_vehicles(self):
        self.board = np.full((6, 6), '.')
        for v in self.vehicles:
            if v.horizontal:
                for i in range(0, v.length):
                    self.board[v.y][v.x+i] = v.letter
            if not v.horizontal:
                for i in range(0, v.length):
                    self.board[v.y+i][v.x] = v.letter

