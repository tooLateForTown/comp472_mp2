from globals import DIRECTION
from Vehicle import Vehicle
import copy


class Move:
    cost = 0
    description = ""
    direction = None
    distance = 0
    board = None
    vehicle = None

    def __init__(self, board, vehicle, direction, distance):
        self.description = f"{vehicle.letter} {direction.name} {distance}"
        self.direction = direction
        self.distance = distance
        self.vehicle = vehicle
        self.board = copy.deepcopy(board)
        self._apply_move_to_board()
        self.move_cost = 1

    def __str__(self):
        return f"{self.description} : {self.board.board_config()}"

    def _apply_move_to_board(self):
        self.board.move_string = self.description
        v = self.board.get_vehicle(self.vehicle.letter)
        if v.horizontal:
            if self.direction == DIRECTION.RIGHT:
                v.x += self.distance
            if self.direction == DIRECTION.LEFT:
                v.x -= self.distance
        if not v.horizontal:
            if self.direction == DIRECTION.DOWN:
                v.y += self.distance
            if self.direction == DIRECTION.UP:
                v.y -= self.distance

        # check if vehicle exited
        if self.board.vehicle_at_exit(v.letter):
            print(f"EXITED: {v}")
            self.board.vehicles.remove(v)
        # rebuild board based on new config
        self.board.rebuild_board_based_on_vehicles()














