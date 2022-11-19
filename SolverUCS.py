from BoardNode import BoardNode
from BoardQueue import BoardQueue

class SolverUCS:

    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.open = BoardQueue()
        self.closed = BoardQueue()
        self.solved = False
        self.finished = False

    def run(self):
        self.open.add(self.initial_board)
        self._loop_until_end()

    def _loop_until_end(self):
        while not self.finished:
            if self.open.is_empty():
                print("Open is empty. No solution found")
                self.finished = True
            else:
                first_open = self.open.pop_first()
                success = self._evaluate_board(first_open)
                if success:
                    print(f"Solution path: {BoardNode.move_path_to_parent(first_open)}")
                if not success:
                    self._add_children_to_open(first_open)
        print("End of program")

    def _evaluate_board(self, board):
        if board.is_goal():
            self.solved = True
            self.finished = True
            print("Board solved!")
            return True
        else:
            # remove from open list and add to closed
            self.open.remove_board(board)
            self.closed.add(board)
            return False


    def _add_children_to_open(self, board):
        # add successor children on board to open
        children = board.get_successor_boards()
        for c in children:
            add_to_open = True
            print(f"{c.move_string} : {c.config_string}")
            duplicate_in_open = self.open.get_board(c.config_string)
            # UCS specific check
            if duplicate_in_open is not None:
                if duplicate_in_open.cost <= c.cost:
                    add_to_open = False
                else:
                    self.open.remove_board(duplicate_in_open)
            duplicate_in_closed = self.closed.get_board(c.config_string)  # todo decide if we also care about cost when doing this
            if duplicate_in_closed is not None:
                add_to_open = False
            if add_to_open:
                self.open.add(c)
        self.open.sort_by_cost()











