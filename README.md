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

- `main.py`: The main implementation of the Tube Puzzle and the A* search algorithm.
- `README.md`: This file.

## How to Run

To run the simulation and see the output, use the following command:

```bash
python main.py
```

## Dependencies

- Python 3.x

## Explanation of the Algorithm

The A* search algorithm is used to solve the Tube Puzzle. The heuristic function guides the search process by estimating the cost to reach the goal from the current state. The heuristic is the maximum of two values:
- `h1`: The number of misplaced colors in the tubes.
- `h2`: The minimum moves required to complete sorting each tube.

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
def a_star(puzzle, verbose=False):
    """Perform the A* search algorithm with optional verbose output for detailed tracing."""
    open_set = []
    heapq.heappush(open_set, (0, puzzle.tubes, [], None))
    visited = set()

    while open_set:
        _, current_state, path, last_move = heapq.heappop(open_set)

        if tuple(map(tuple, current_state)) in visited:
            continue
        visited.add(tuple(map(tuple, current_state)))

        if puzzle.is_goal():
            if verbose:
                print("Goal Reached!")
            return path

        moves = puzzle.find_moves()
        if not moves and verbose:
            print("No available moves. Stuck state reached.")

        for move in moves:
            if last_move and move == (last_move[1], last_move[0]):
                continue

            new_state = [list(tube) for tube in current_state]
            color = new_state[move[0]].pop()
            new_state[move[1]].append(color)
            new_path = path + [move]
            score = len(new_path) + heuristic(new_state, puzzle.tube_capacity)
            heapq.heappush(open_set, (score, new_state, new_path, move))

            if verbose:
                print(f"Move from Tube {move[0] + 1} to Tube {move[1] + 1} considered. New state:")
                for idx, tube in enumerate(new_state):
                    print(f"Tube {idx + 1}: {tube}")


def generate_random_initial_matrix(num_tubes, tube_capacity, max_color):
    """Generate a random initial matrix for the puzzle with specified parameters."""
    tubes = []
    colors = [random.randint(1, max_color) for _ in
              range(num_tubes * tube_capacity - random.randint(1, num_tubes))]  # Ensure some emptiness
    random.shuffle(colors)
    for i in range(0, len(colors), tube_capacity):
        tubes.append(colors[i:i + tube_capacity])
    while len(tubes) < num_tubes:
        tubes.append([])  # Ensure there are empty tubes
    return tubes


def main_simulation():
    """Run multiple iterations of the puzzle solver with random initial configurations."""
    num_iterations = 20
    for i in range(num_iterations):
        num_tubes = random.randint(5, 10)
        tube_capacity = random.randint(3, 5)
        max_color = 5
        initial_matrix = generate_random_initial_matrix(num_tubes, tube_capacity, max_color)
        puzzle = TubePuzzle(initial_matrix=initial_matrix)
        print(f"Initial configuration for iteration {i + 1}:")
        puzzle.display_tubes()
        solution = a_star(puzzle, verbose=True)
        print("Solution Steps:", solution)
        print("------------------------------------------------------")


if __name__ == "__main__":
    main_simulation()
```

## Usage

1. **Initialization**: Create a `TubePuzzle` instance with a predefined matrix or random configuration.
2. **Heuristic Calculation**: Use the `heuristic` function to estimate the cost.
3. **A* Algorithm**: Run the `a_star` function to find the solution path.
4. **Simulation**: Use the `main_simulation` function to run multiple iterations with random configurations.

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
