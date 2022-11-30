from BoardNode import BoardNode
from globals import HEURISTIC, ALGORITHM


class BoardQueue:

    def __init__(self):
        self.nodes = []   # of type BoardNode

    # def sort_by_cost(self):  # for UCS
    #     self.nodes.sort(key=lambda x: x.cost)

    def get_board(self, config_string):
        # returns board if found.  Useful for removing for UCS
        for b in self.nodes:
            if b.config_string == config_string:
                return b
        return None

    def add(self, board):
        self.nodes.append(board)

    def pop_first(self):
        if len(self.nodes) == 0:
            return None
        else:
            return self.nodes.pop(0)

    def is_empty(self):
        return len(self.nodes) == 0

    def remove_board(self, board):
        # removes all copies of board with same config_string
        to_remove = []
        for b in self.nodes:
            if b.config_string == board.config_string:
                to_remove.append(b)
        for b in to_remove:
            self.nodes.remove(b)

    def sort_by_heuristic(self, heuristic, algorithm, lambda_val):
        if algorithm == ALGORITHM.UCS:
            self.nodes.sort(key=lambda x: x.cost)
        elif algorithm == ALGORITHM.GBFS:
            if heuristic == HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES:
                self.nodes.sort(key=lambda x: x.number_of_blocking_vehicles())
            if heuristic == HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS:
                self.nodes.sort(key=lambda x: x.number_of_blocked_positions())
            if heuristic == HEURISTIC.H3_H1_TIMES_LAMBDA:
                self.nodes.sort(key=lambda x: x.number_of_blocking_vehicles() * lambda_val)
            # if heuristic == HEURISTIC.H4_CUSTOM: #todo turn this back omn
            #     self.nodes.sort(key=lambda x: x.custom_heuristic)
        elif algorithm == ALGORITHM.A:
            if heuristic == HEURISTIC.H1_NUMBER_BLOCKING_VEHICLES:
                self.nodes.sort(key=lambda x: x.cost + x.number_of_blocking_vehicles())
            if heuristic == HEURISTIC.H2_NUMBER_BLOCKED_POSITIONS:
                self.nodes.sort(key=lambda x: x.cost + x.number_of_blocked_positions())
            if heuristic == HEURISTIC.H3_H1_TIMES_LAMBDA:
                self.nodes.sort(key=lambda x: (x.cost + x.number_of_blocking_vehicles()) * lambda_val)
            # if heuristic == HEURISTIC.H4_CUSTOM:  # todo turn this on
            #     self.nodes.sort(key=lambda x: x.cost + x.custom_heuristic)


    











