from BoardNode import BoardNode
from BoardQueue import BoardQueue

class SolverUCS:

    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.open = BoardQueue()
        self.closed = BoardQueue()
        self.solved = False

    def run(self):
        self.open.add(self.initial_board)
        self._loop_until_end()

    def _loop_until_end(self):
        if self.open.is_empty():
            print("Open is empty. No solution found")
            return
        self._evaluate_board(self.open.pop_first())

    def _evaluate_board(self, board):
        if board.is_goal():
            self.solved = True
            print("Board solved!")
        else:
            children = board.get_successor_boards()
            for c in children:
                print(f"{c.move_string} : {c.config_string}")









