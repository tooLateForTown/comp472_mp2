import globals
from globals import DIRECTION
from Vehicle import Vehicle
import copy


class BoardNode:
    valid = False

    def __init__(self, config):  # eg: BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.
        self.vehicles = []
        self.board = ""
        self.cost = 0
        self.config_string = "to fill in to save computation time while iterating"
        self.parent = None
        self.depth = 0  # graph node depth
        self.runtime = 0
        # move specific info
        self.move_string = "Start"
        self.vehicle_moved = '?'
        self.vehicle_gas_after_move = 0
        self.vehicle_direction = None
        self.vehicle_distance = 0
        self.h = -1
        self.valid = self.load_game(config)

    def getYX(self, y, x):
        return self.board[y * 6 + x]

    def setYX(self, y, x, c):
        self.board = self.board[:y*6+x] + c + self.board[y*6+x+1:]

    def load_game(self, config) -> bool:
        config = config.strip()
        if len(config) < 36:
            print("Setup needs to be at least 36 characters")
            return False
        # load Board array
        for row in range(0, 6):
            for col in range(0, 6):
                self.setYX(row, col, config[row * 6 + col])
                # self.board[row][col] = config[row * 6 + col]
        # identify the vehicles
        for row in range(0, 6):
            for col in range(0, 6):
                letter = self.getYX(row, col)
                # letter = self.board[row][col]
                if letter != '.':
                    vehicle = self.get_vehicle(letter)
                    if vehicle is None:
                        v = Vehicle(letter)
                        v.x = col  # top left posit
                        v.y = row
                        # determine length and direction
                        if row < 5 and self.getYX(row + 1, col) == letter:
                        # if row < 5 and self.board[row + 1][col] == letter:
                            v.horizontal = False
                            temp_y = row
                            while temp_y <= 5 and self.getYX(temp_y, col) == letter:
                            # while temp_y <= 5 and self.board[temp_y][col] == letter:
                                v.length += 1
                                temp_y += 1
                        elif col < 5 and self.getYX(row, col+1) == letter:
                        # elif col < 5 and self.board[row][col + 1] == letter:
                            v.horizontal = True
                            temp_x = col
                            while temp_x <= 5 and self.getYX(row, temp_x) == letter:
                            # while temp_x <= 5 and self.board[row][temp_x] == letter:
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
        return v.horizontal and v.get_right() >= 5 and v.y == 2

    def get_vehicle(self, letter) -> Vehicle:
        for v in self.vehicles:
            if v.letter == letter:
                return v
        return None

    def show_board(self, show_vehicles=True):
        print('   a b c d e f')
        print("  -------------")
        count = 1
        for row in range(0, 6):
        # for row in self.board:
            print(count, end='| ')
            count += 1
            for col in range(0, 6):
                print(self.board[row*6+col:row*6+col+1], end=' ')
            # for col in row:
            #     print(col, end=' ')
            print()
        print("  -------------")
        print(f"{len(self.vehicles)} vehicles: ", end='')
        if show_vehicles:
            for v in self.vehicles:
                print(v, end=' ')
        print()

    def string_of_board(self):
        s = ""
        for row in range(0,6):
            for col in range(0,6):
                s += self.board[row*6 + col]
            s += "\n"
        # for row in self.board:
        #     for col in row:
        #         s += col
        #     s += "\n"
        return s

    def board_config_string(self, include_gas=False):
        # long string used to represent entire board state.
        # eg:  IJBBCCIJDDL.IJAAL.EEK.L...KFF..GGHH. F0 G6
        # note that this does NOT include cost, search history, etc...
        s = ""
        for row in self.board:
            for col in row:
                s += col
        # gas values
        if include_gas:
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

        if direction == DIRECTION.up:
            y -= 1
            while y >= 0 and self.getYX(y, x) == '.':
            # while y >= 0 and self.board[y][x] == '.':
                count += 1
                y -= 1
        if direction == DIRECTION.down:
            y += 1
            while y <= 5 and self.getYX(y, x) == '.':
            # while y <= 5 and self.board[y][x] == '.':
                count += 1
                y += 1
        if direction == DIRECTION.right:
            x += 1
            while x <= 5 and self.getYX(y, x) == '.':
            # while x <= 5 and self.board[y][x] == '.':
                count += 1
                x += 1
        if direction == DIRECTION.left:
            x -= 1
            while x >= 0 and self.getYX(y, x) == '.':
            # while x >= 0 and self.board[y][x] == '.':
                count += 1
                x -= 1

        return count

    def get_successor_boards(self):  # SUCCESSOR FUNCTION
        children = []
        # print("Searching for all valid moves....")
        for v in self.vehicles:
            if v.horizontal:
                for i in range(0, self.number_free_spaces(v.x + v.length - 1, v.y, DIRECTION.right)):
                    b = self.single_move_result(v, DIRECTION.right, i + 1)
                    if b.vehicle_gas_after_move >= 0:
                        children.append(b)
                for i in range(0, self.number_free_spaces(v.x, v.y, DIRECTION.left)):
                    b = self.single_move_result(v, DIRECTION.left, i + 1)
                    if b.vehicle_gas_after_move >= 0:
                        children.append(b)
            if not v.horizontal:
                for i in range(0, self.number_free_spaces(v.x, v.y, DIRECTION.up)):
                    b = self.single_move_result(v, DIRECTION.up, i + 1)
                    if b.vehicle_gas_after_move >= 0:
                        children.append(b)
                for i in range(0, self.number_free_spaces(v.x, v.y + v.length - 1, DIRECTION.down)):
                    b = self.single_move_result(v, DIRECTION.down, i + 1)
                    if b.vehicle_gas_after_move >= 0:
                        children.append(b)
        return children

    def single_move_result(self, vehicle, direction, distance):
        child_board = copy.deepcopy(
            self)  # todo consider throwing away vechicles before deep-cloning to avoid filling memory
        child_board.vehicle_moved = vehicle.letter
        child_board.vehicle_direction = direction
        child_board.vehicle_distance = distance
        v = child_board.get_vehicle(vehicle.letter)
        v.gas -= distance
        child_board.vehicle_gas_after_move = v.gas
        if v.horizontal:
            if direction == DIRECTION.right:
                v.x += distance
            if direction == DIRECTION.left:
                v.x -= distance
        if not v.horizontal:
            if direction == DIRECTION.down:
                v.y += distance
            if direction == DIRECTION.up:
                v.y -= distance

        # check if vehicle exited (except the ambulance)
        if v.letter != 'A':
            if child_board.vehicle_at_exit(v.letter):
                # print(f"EXITED: {v}")
                child_board.vehicles.remove(v)

        child_board.rebuild_board_based_on_vehicles()  # rebuild board based on new config
        # add child-specific values
        child_board.move_string = f"{vehicle.letter} {direction.name} {distance}"
        child_board.config_string = child_board.board_config_string()  # only calculate config string once
        # TODO: Calculate cost depending on algorithm, cost and depth should be different!
        child_board.cost += 1  # todo check that this is right
        child_board.depth += 1
        child_board.parent = self
        return child_board

    def rebuild_board_based_on_vehicles(self):
        self.board = "...................................."
        for v in self.vehicles:
            if v.horizontal:
                for i in range(0, v.length):
                    self.setYX(v.y, v.x + i, v.letter)
                    # self.board[v.y][v.x + i] = v.letter
            if not v.horizontal:
                for i in range(0, v.length):
                    self.setYX(v.y+i, v.x, v.letter)
                    # self.board[v.y + i][v.x] = v.letter

    @staticmethod
    def path_to_parent(end_board):
        path = []
        if end_board.parent is None:
            # we bizarrely started at the parent.  return nothing
            return []
        path.append(end_board)
        parent = end_board.parent
        while parent.parent is not None:
            path.insert(0, parent)
            parent = parent.parent
        return path

    def string_for_solution(self):
        return f"{self.vehicle_moved} {str(self.vehicle_direction.name).rjust(5)} {self.vehicle_distance} {str(self.vehicle_gas_after_move).rjust(6)} {self.config_string}"

    def string_for_searchpath(self):
        return f"{self.h + self.cost} {self.cost} {self.h} {self.config_string}"

    def number_of_blocking_vehicles(self):
        # returns the number of vehicles that are blocking the ambulance
        ambulance_right_position = self.get_vehicle('A').get_right()
        found_vehicles = set()
        for x in range(ambulance_right_position + 1, 6):
            if self.getYX(2, x) != '.':
                found_vehicles.add(self.getYX(2, x))
            # if self.board[2][x] != '.':
            #     found_vehicles.add(self.board[2][x])
        # print(found_vehicles)
        # if found_vehicles == {'L','K'}:
        #     self.show_board(True)
        return len(found_vehicles)

    def number_of_blocked_positions(self):
        # returns the number of positions that are non-empty between the ambulance and the exit on row 2
        count = 0
        amb = self.get_vehicle('A')
        for x in range(amb.get_right() + 1, 6):
            if self.getYX(2, x) != '.':
            # if self.board[2][x] != '.':
                count += 1
        return count

    def manhattan_distance(self):
        # returns the distance between vehicle A and the exit. The exit is at (5,2)
        amb = self.get_vehicle('A')
        return abs(amb.get_right() - 5)

    def number_of_blocked_positions_in_area_to_right_of_ambulance_edge(self):
        count = 0
        amb = self.get_vehicle('A')
        for y in range(0, 6):
            for x in range(amb.get_right() + 1, 6):
                if self.getYX(y, x) != '.':
                # if self.board[y][x] != '.':
                    count += 1
        return count

    def car_fuel_for_output(self):
        s = ""
        for v in self.vehicles:
            if s != "":
                s += ", "
            s += f"{v.letter}:{v.gas}"
        return s