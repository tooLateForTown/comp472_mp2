from BoardNode import BoardNode


class BoardQueue:

    def __init__(self):
        self.nodes = []   # of type BoardNode

    def sort_by_cost(self):  # for UCS
        self.nodes.sort(key=lambda x: x.cost)

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

    def sort_by_heuristic(self, heuristic):
        # heuristic map
        # 1: number of blocking vehicles
        heuristic_dict = {'number_of_blocking_vehciles': 1, 'number_of_blocked_positions': 2, 'blocking_vehicles_and_distance_and_gas': 3}

        # Sort by cost + heuristic
        if heuristic_dict[heuristic] == 1:
            self.nodes.sort(key=lambda x: x.cost + x.number_of_blocking_vehciles())
        elif heuristic_dict[heuristic] == 2:
            self.nodes.sort(key=lambda x: x.cost + x.number_of_blocked_positions())
    











