# Tube Puzzle Solver

This project implements a solver for the Tube Puzzle using the A* search algorithm. The puzzle involves a set of tubes filled with colors, and the goal is to sort the colors such that each tube contains only one color.

## Table of Contents

- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Dependencies](#dependencies)
- [Explanation of the Algorithm](#explanation-of-the-algorithm)
- [Usage](#usage)
- [Example](#example)

## Project Structure

- `LiquidPuzzle.py`: The main implementation of the Tube Puzzle and the A* search algorithm.
- `README.md`: This file.

## How to Run

To run the simulation and see the output, use the following command:

```bash
python LiquidPuzzle.py
```

## Dependencies

- Python 3.x

## Explanation of the Algorithm

The A* search algorithm is used to solve the Tube Puzzle. The heuristic function guides the search process by estimating the cost to reach the goal from the current state.

### Key Functions

#### `TubePuzzle`

The `TubePuzzle` class initializes the puzzle either with a predefined matrix or by generating a random configuration. It includes methods to display the current state, check the goal state, find legal moves, and make moves.

#### `heuristic`

```python
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
        # Calculate the heuristic value
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
```

#### `a_star`

```python
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
```
## Example

To see the solver in action, run the `main_simulation` function. This will generate random initial configurations and attempt to solve each one, printing the steps and the final solution.

```bash
python main.py
```

Output will display the initial state, the considered moves, intermediate states, and the solution steps.

```plaintext
Initial configuration for iteration 1:
Tube 1: [1, 2, 2]
Tube 2: [1, 1]
Tube 3: [2]
Tube 4: Empty
Tube 5: [2, 2, 2]
Tube 6: Empty
...
Solution Steps: [(0, 4), (2, 5), ...]
------------------------------------------------------
```

This project provides a complete implementation of a Tube Puzzle solver using the A* search algorithm, with detailed logging and a heuristic function to guide the search.
