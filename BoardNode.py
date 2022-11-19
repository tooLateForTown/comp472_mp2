import numpy as np

import globals
from globals import DIRECTION
from Vehicle import Vehicle
import copy


class BoardNode:
    valid = False

    def __init__(self, config):
        self.vehicles = []
        self.board = np.full((6, 6), '.')
        self.valid = self.load_game(config)
        self.move_string = "Start"
        self.cost = 0
        self.config_string ="to fill in to save computation time while iterating"
        self.parent = None

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
                    self.vehicles.sort(key=BoardNode.letter_val)
        # load gas from config string
        if len(config) > 36:
            for gas in config[36:].split(' '):
                if len(gas) > 1:
                    v = self.get_vehicle(gas[0])
                    if v is None:
                        print("Gas setup referring to vehicle not previously found.")
                        return False
                    print(f"Gas found for {v.letter}")
                    v.gas = int(gas[1:])
        self.config_string = self.board_config_string()
        self.cost = 0
        self.parent = None
        return True

    def is_goal(self):
        return self.vehicle_at_exit('A')

    def vehicle_at_exit(self, letter):
        # only horizontal vehicles can exit
        v = self.get_vehicle(letter)
        return v.horizontal and v.get_right() >= 5

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

    def board_config_string(self):
        # long string used to represent entire board state.
        # eg:  IJBBCCIJDDL.IJAAL.EEK.L...KFF..GGHH. F0 G6
        # note that this does NOT include cost, search history, etc...
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

    def get_successor_boards(self):  # SUCCESSOR FUNCTION
        children = []
        print("Searching for all valid moves....")
        # todo:  Check if newly generated move has already been considered (in the state space)
        # todo: if so, don't add it again.  So must check every time before appeneding (video 1, 36:00)
        # todo:  will need to construct graph of nodes

        for v in self.vehicles:
            if v.horizontal:
                for i in range(0, self.number_free_spaces(v.x + v.length - 1, v.y, DIRECTION.RIGHT)):
                    b = self.single_move_result(v, DIRECTION.RIGHT, i + 1)
                    children.append(b)
                for i in range(0, self.number_free_spaces(v.x, v.y, DIRECTION.LEFT)):
                    b = self.single_move_result( v, DIRECTION.LEFT, i + 1)
                    children.append(b)
            if not v.horizontal:
                for i in range(0, self.number_free_spaces(v.x, v.y, DIRECTION.UP)):
                    b = self.single_move_result(v, DIRECTION.UP, i + 1)
                    children.append(b)
                for i in range(0, self.number_free_spaces(v.x, v.y + v.length - 1, DIRECTION.DOWN)):
                    b = self.single_move_result(v, DIRECTION.DOWN, i + 1)
                    children.append(b)
        return children


    def single_move_result(self, vehicle, direction, distance):
        child_board = copy.deepcopy(self)
        child_board.move_string = f"{vehicle.letter} {direction.name} {distance}"
        v = child_board.get_vehicle(vehicle.letter)
        if v.horizontal:
            if direction == DIRECTION.RIGHT:
                v.x += distance
            if direction == DIRECTION.LEFT:
                v.x -= distance
        if not v.horizontal:
            if direction == DIRECTION.DOWN:
                v.y += distance
            if direction == DIRECTION.UP:
                v.y -= distance

        # check if vehicle exited (except the ambulance)
        if v.letter != 'A':
            if child_board.vehicle_at_exit(v.letter):
                print(f"EXITED: {v}")
                child_board.vehicles.remove(v)
        # rebuild board based on new config
        child_board.rebuild_board_based_on_vehicles()
        child_board.config_string = child_board.board_config_string()  # only calculate config string once
        return child_board


    def rebuild_board_based_on_vehicles(self):
        self.board = np.full((6, 6), '.')
        for v in self.vehicles:
            if v.horizontal:
                for i in range(0, v.length):
                    self.board[v.y][v.x+i] = v.letter
            if not v.horizontal:
                for i in range(0, v.length):
                    self.board[v.y+i][v.x] = v.letter

