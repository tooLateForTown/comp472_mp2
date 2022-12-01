import os
import globals

# DEFAULT_INPUT_FOLDER = "input"


def choose_input_file():
    dir_list = os.listdir(globals.INPUT_FOLDER)
    file_count = len(dir_list)
    print(f"Choose file to load from /{globals.INPUT_FOLDER}, (q to quit)")
    counter = 0
    for d in dir_list:
        print(f"{counter:<3}{d}")
        counter += 1

    aborted = False
    selected = -1
    while not aborted and selected == -1:
        choice = input("Entry: ")
        if choice.lower() == 'q':
            print("Bye")
            exit()
        if choice.isnumeric():
            if int(choice) >=0 and int(choice) < file_count:
                selected = int(choice)

    print(f"You selected: {dir_list[selected]}")
    return process_input_file(f"{globals.INPUT_FOLDER}/{dir_list[selected]}")

def process_input_file(file_name):
    # returns a list of puzzles
    puzzles = []
    with open(file_name,'r') as f:
        for line in f:
            line = line.strip()
            if line == "":
                print("(Skipped blank)")
            elif line[0] == '#':
                print(f"(Skipped {line})")
            else:
                print(f"Good: {line}")
                puzzles.append(line)
    return puzzles














