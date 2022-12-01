from enum import Enum

DEFAULT_GAS = 100
INPUT_FOLDER = "input"
FIFTY_PUZZLES_FILE = "puzzles50.txt"
OUTPUT_FOLDER = "output"

analysis_csv = ""


class DIRECTION(Enum):
    up = 1
    right = 2
    down = 3
    left = 4


class HEURISTIC(Enum):
    H0_PURELY_COST_FOR_UCS = 0
    H1_NUMBER_BLOCKING_VEHICLES = 1
    H2_NUMBER_BLOCKED_POSITIONS = 2
    H3_H1_TIMES_LAMBDA = 3
    H4_CUSTOM = 4


class ALGORITHM(Enum):
    UCS = 0
    GBFS = 1
    A = 2
