from BoardNode import BoardNode


class BoardQueue:

    def __init__(self):
        self.nodes = []   # of type BoardNode

    def sort_by_cost(self):  # for UCS
        self.nodes.sort(key=BoardNode.cost)

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

    def remove_board(self, board, only_remove_higher_cost_variant = False):
        to_remove = []
        for b in self.nodes:
            if b.config_string == board.config_string:
                if only_remove_higher_cost_variant:
                    if b.cost > board.cost:
                        to_remove.append(b)
                else:
                    to_remove.append(b)
        for b in to_remove:
            self.nodes.remove(b)









