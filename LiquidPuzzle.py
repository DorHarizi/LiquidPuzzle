import heapq
import copy
import itertools
import time
import pandas as pd

start_time = -1
time_passed = -1


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, priority, item):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)


class ColorSortPuzzle:
    def __init__(self):
        self.containers = []
        self.fill_levels = []
        self.conflicts = {}
        self.top_colors = {}
        self.sum_of_blocks = 0
        self.empty = -1
        self.full = -1
        self.size = -1
        self.colors = -1
        self.num_of_state = 0
        self.cur_empty = -1
        self.src_tube = -1
        self.dest_tube = -1
        self.key = ""
        self.log_game = ""
        self.fx = -1

    def __lt__(self, other):
        return self.fx < other.fx

    def initial_state(self, empty, full, size, init, colors):
        self.empty = empty
        self.cur_empty = empty
        self.full = full
        self.size = size
        self.colors = colors
        self.containers = init
        self.operators = []
        self.fill_levels = [len(tube) for tube in self.containers]
        self.num_of_state = 0
        self.key = repr(self.containers)
        self.log_game = ""
        self.src_tube = -1
        self.dest_tube = -1
        self.fx = -1
        self.sum_of_blocks = 0
        for index_tube in range(len(self.containers)):
            if self.containers[index_tube]:
                self.sum_of_blocks += 1
                last_color = self.containers[index_tube][0]
                for color in self.containers[index_tube]:
                    if color != last_color:
                        self.sum_of_blocks += 1
                    last_color = color
            self.conflicts[index_tube] = len(set(self.containers[index_tube]))

            if self.containers[index_tube]:
                color_src = self.containers[index_tube][0]
                color_counter = 0
                for index in range(len(self.containers[index_tube])):
                    if color_src == self.containers[index_tube][index]:
                        color_counter += 1
                    else:
                        break
                self.top_colors[index_tube] = (color_src, color_counter)
            else:
                self.top_colors[index_tube] = -1

    def print_current_state(self) -> None:
        print(f"Puzzle State: {self.num_of_state}")
        print(f"Containers: {self.containers}")
        print(f"last move is: {self.src_tube} -> {self.dest_tube}")

    def is_goal(self):
        global time_passed, start_time
        time_passed = time.time() - start_time
        # Check if the number of empty tubes matches the desired empty tubes
        if self.cur_empty != self.empty:
            return False

        # Check if all non-empty tubes contain only blocks of the same color
        for tube in self.containers:
            if tube and len(set(tube)) != 1:
                return False
        return True

    def is_move(self, src, dest):
        if not self.containers[src]:    # check if src is not empty
            return False

        if not self.containers[dest]:   # check if dest is not empty
            return True

        if len(self.containers[dest]) == self.size:
            return False
        color = self.top_colors[src]
        if isinstance(color, tuple):
            if self.top_colors[src][1] > self.size - len(self.containers[dest]):
                return False
        return True

    def is_move_manual(self, src, dest):
        if not self.containers[src]:    # check if src is not empty
            return False

        if not self.containers[dest]:   # check if dest is not empty
            return True

        if len(self.containers[dest]) == self.size:
            return False

        if self.containers[src][0] != self.containers[dest][0]:
            return False

        color = self.top_colors[src]
        if isinstance(color, tuple):
            if self.top_colors[src][1] > self.size - len(self.containers[dest]):
                return False
        return True

    def move(self, src, dest):
        self.src_tube, self.dest_tube = src, dest
        self.sum_of_blocks -= 1
        if self.conflicts[src] == 1:
            self.cur_empty += 1
        if not self.containers[dest]:
            self.sum_of_blocks += 1
            self.cur_empty -= 1

        if not self.containers[dest]:
            self.containers[dest].insert(0, self.containers[src].pop(0))
        while self.containers[src] and len(self.containers[dest]) < self.size and self.containers[src][0] == \
                self.containers[dest][0]:
            self.containers[dest].insert(0, self.containers[src].pop(0))
        self.update_move()

    def update_move(self):
        self.num_of_state += 1
        src, dest = self.src_tube, self.dest_tube
        self.key = repr(self.containers)
        self.log_game += f"\n{src} -> {dest}\n"

        self.conflicts[src] = len(set(self.containers[src]))
        self.conflicts[dest] = len(set(self.containers[dest]))

        if self.containers[src]:
            color_src = self.containers[src][0]
            color_counter = 1
            for i in range(1, len(self.containers[src])):
                if color_src == self.containers[src][i]:
                    color_counter += 1
                else:
                    break
            self.top_colors[src] = (color_src, color_counter)
        else:
            self.top_colors[src] = -1

        if self.containers[dest]:
            color_dest = self.containers[dest][0]
            color_counter = 1
            for i in range(1, len(self.containers[dest])):
                if color_dest == self.containers[dest][i]:
                    color_counter += 1
                else:
                    break
            self.top_colors[dest] = (color_dest, color_counter)
        else:
            self.top_colors[dest] = -1
        self.fill_levels[self.src_tube] = len(self.containers[self.src_tube])
        self.fill_levels[self.dest_tube] = len(self.containers[self.dest_tube])
        self.fx = (0.10 * self.cur_empty) + (0.30 * self.sum_of_blocks) + (0.40 * self.calculate_misplaced_units()) + (
                    0.20 * self.calculate_fill_level_difference())

    def calculate_misplaced_units(self):
        misplaced_units = 0
        for tube in self.containers:
            if len(tube) > 1:
                tube_set = set(tube)
                max_count = max(tube.count(color) for color in tube_set)
                misplaced_units += len(tube) - max_count
        return misplaced_units

    def calculate_fill_level_difference(self):
        # Calculate the difference in fill levels between tubes
        max_fill = max(self.fill_levels)
        min_fill = min(self.fill_levels)
        return max_fill - min_fill

    def generate_moves(self):
        self.operators = []
        optional_operators = {}
        for color in range(self.colors):
            optional_operators[color] = []
        empty_tube_index = -1
        is_empty = False
        for index_tube, value in self.top_colors.items():
            if isinstance(value, tuple):
                optional_operators[value[0]].append(index_tube)
            else:
                is_empty = True
                empty_tube_index = index_tube
        if is_empty:
            for color_tubes in optional_operators.values():
                color_tubes.append(empty_tube_index)

        for color_list in optional_operators.values():
            for move in itertools.permutations(color_list, 2):
                src, dest = move
                if self.is_move(src, dest):
                    if len(set(self.containers[src])) == 1 and len(set(self.containers[dest])) == 1:
                        self.operators.clear()
                        self.operators.append(move)
                        return
                    if len(set(self.containers[src])) != 1 or self.containers[dest]:
                        self.operators.append(move)

    def a_star(self):
        global start_time
        start_time = time.time()
        open_list = PriorityQueue()
        closed_list = {}
        state_lookup = {}
        self.fx = (0.10 * self.cur_empty) + (0.30 * self.sum_of_blocks) + (0.40 * self.calculate_misplaced_units()) + (
                    0.20 * self.calculate_fill_level_difference())
        open_list.put(self.fx, self)
        state_lookup[self.key] = self
        while not open_list.empty():
            current_state_fx, current_state = open_list.get()
            assert isinstance(current_state, ColorSortPuzzle)
            if current_state.key in state_lookup:
                state_lookup.pop(current_state.key)

            if current_state.is_goal():
                print("\n-----------------------------------------------------------")
                print("Goal State Reached!")
                print(f"{current_state.log_game}")
                return current_state.num_of_state

            closed_list[current_state.key] = current_state
            current_state.generate_moves()
            for operator in current_state.operators:
                child_state = copy.deepcopy(current_state)
                child_state.move(operator[0], operator[1])
                if child_state.key not in closed_list and child_state.key not in state_lookup:
                    open_list.put(child_state.fx, child_state)
                    state_lookup[child_state.key] = child_state
                elif child_state.key in state_lookup:
                    if state_lookup[child_state.key].fx > child_state.fx:
                        state_lookup[child_state.key] = child_state
                        open_list.put(child_state.fx, child_state)
        return -1


if __name__ == "__main__":
    print("Welcome to the solver Liquid Puzzle")
    while True:
        tmp = input("If you want to solve the problem automatically, press 1. Else, press 0: ")
        if tmp == "1":
            auto_solve = True
            break
        elif tmp == "0":
            auto_solve = False
            break
        else:
            print("Invalid input. Please enter 1 or 0.")
    try:
        with open("instances.txt", 'r') as file:
            content = file.read().splitlines()
    except FileNotFoundError:
        print("The file instances.txt was not found.")
        exit(1)

    line = 0
    cases = []

    while line < len(content):
        try:
            case_num = int(content[line].replace('#', ''))
            empty = int(content[line + 1].split(' ')[-1])
            full = int(content[line + 2].split(' ')[-1])
            size = int(content[line + 3].split(' ')[-1])
            colors = int(content[line + 4].split(' ')[-1])
            init = eval(content[line + 5].split('=')[1])
        except (IndexError, ValueError):
            print(f"Error reading case starting at line {line + 1}. Skipping case.")
            line += 7
            continue

        obj = ColorSortPuzzle()
        obj.initial_state(empty=empty, full=full, size=size, colors=colors, init=init)
        num_of_state = 0
        if auto_solve:
            num_of_state = obj.a_star()
        else:
            while not obj.is_goal():
                obj.print_current_state()
                try:
                    src_tube = int(input("Please choose the source tube: "))
                    dest_tube = int(input("Please choose the destination tube: "))
                except ValueError:
                    print("Invalid input. Please enter valid tube indices.")
                    continue
                if obj.is_move_manual(src_tube, dest_tube):
                    obj.move(src_tube, dest_tube)
                    num_of_state += 1
                else:
                    print("\nInvalid move.\nPlease enter a new choice.\n")
        print(f"\n-----Well done, you solved test number {case_num}-----\n")
        cases.append([case_num, num_of_state, time_passed])
        line += 7  # go to next case line

    # Create and display the runtime
    columns = ["Case Number", "Steps Number", "Runtime (s)"]
    df = pd.DataFrame(cases, columns=columns)
    styled_df = df.style.apply(lambda _: ['font-weight: bold'], subset=pd.IndexSlice[0, :]).set_properties(**{'text-align': 'center'}).applymap(lambda x: 'color: red', subset=pd.IndexSlice[:, columns[0]])
    styled_df.to_excel("output.xlsx", engine='openpyxl', index=False)
    print("\nData has been saved to output.xlsx")
