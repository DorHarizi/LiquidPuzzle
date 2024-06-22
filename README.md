# Liquid Puzzle Solver

This project provides a solver for the Liquid Puzzle game, where the objective is to sort liquids of different colors into separate tubes. The solver uses the A* algorithm to find the solution efficiently.

## Project Structure

- `LiquidPuzzle.py`: Contains the main implementation of the Liquid Puzzle solver, including the A* algorithm, the `ColorSortPuzzle` class, and the `PriorityQueue` class.
- `instances.txt`: Input file containing various test cases for the Liquid Puzzle solver.
- `finel_result.xlsx`: Output file with the results of the solver's execution on the instances.
- `test.py`: Script for testing the solver with the provided instances.
- `Project_Specifications.pdf`: Detailed description of the project requirements and specifications in Hebrew.

## How to Run

1. Ensure you have Python installed on your system.
2. Install the required dependencies:
   ```bash
   pip install pandas openpyxl
   ```
3. Place the `instances.txt` file in the same directory as `LiquidPuzzle.py`.
4. Run the solver:
   ```bash
   python LiquidPuzzle.py
   ```
5. The results will be saved in `finel_result.xlsx`.

## Dependencies

- Python 3.x
- Pandas
- Openpyxl

## Explanation of the Algorithm

The solver uses the A* algorithm to find the solution for the Liquid Puzzle game. The A* algorithm is a popular search algorithm that combines the strengths of Dijkstra's Algorithm and Greedy Best-First-Search. It uses a heuristic to estimate the cost of reaching the goal from the current state and prioritizes states with the lowest estimated cost.

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

### Heuristic Function

The heuristic function used in this project is a combination of four factors, each contributing to the estimated cost (`fx`) of reaching the goal state from the current state:

```python
self.fx = (0.10 * self.cur_empty) + (0.30 * self.sum_of_blocks) + (0.40 * self.calculate_misplaced_units()) + (0.20 * self.calculate_fill_level_difference())
```

- `self.cur_empty`: The number of currently empty tubes. More empty tubes generally make it easier to move and organize the blocks, so this factor is given a weight of 10%.
- `self.sum_of_blocks`: The sum of different colored blocks in the tubes. It helps in assessing how disorganized the current state is. This factor is given a weight of 30%.
- `self.calculate_misplaced_units()`: The number of misplaced units in the tubes. A misplaced unit is a block that is not grouped with blocks of the same color. This factor is crucial as it directly impacts the goal of having each tube containing only blocks of the same color. It is given the highest weight of 40%.
- `self.calculate_fill_level_difference()`: The difference in fill levels between the most and least filled tubes. A smaller difference generally indicates a more balanced distribution of blocks, making it easier to achieve the goal state. This factor is given a weight of 20%.

### Calculating Misplaced Units

The `calculate_misplaced_units` function calculates the number of misplaced units in the tubes. A misplaced unit is a block that is not grouped with blocks of the same color:

```python
def calculate_misplaced_units(self):
    misplaced_units = 0
    for tube in self.containers:
        if len(tube) > 1:
            tube_set = set(tube)
            max_count = max(tube.count(color) for color in tube_set)
            misplaced_units += len(tube) - max_count
    return misplaced_units
```

### Calculating Fill Level Difference

The `calculate_fill_level_difference` function calculates the difference in fill levels between the most and least filled tubes:

```python
def calculate_fill_level_difference(self):
    max_fill = max(self.fill_levels)
    min_fill = min(self.fill_levels)
    return max_fill - min_fill
```

### Key Classes and Methods

- `PriorityQueue`: A simple priority queue implementation using a heap.
- `ColorSortPuzzle`: Represents the puzzle state and provides methods for initializing the puzzle, checking the goal state, generating possible moves, and executing moves.
- `initial_state()`: Initializes the puzzle with the given parameters.
- `is_goal()`: Checks if the current state is the goal state.
- `is_move()`: Validates if a move from one tube to another is possible.
- `move()`: Executes a move from one tube to another.
- `generate_moves()`: Generates all possible moves from the current state.
- `a_star()`: Implements the A* algorithm to solve the puzzle.

## Usage

The solver can be used in two modes: automatic and manual.

- Automatic Mode: The solver automatically finds the solution using the A* algorithm.
- Manual Mode: The user can manually input moves to solve the puzzle.

### Running in Automatic Mode

To run the solver in automatic mode, press `1` when prompted at the beginning of the script execution. The solver will automatically read the instances from `instances.txt` and solve them.

### Running in Manual Mode

To run the solver in manual mode, press `0` when prompted. The solver will display the current state of the puzzle and prompt the user to input the source and destination tubes for each move.

## Example

Here is an example of the input format in `instances.txt`:

```
##########################0################################
empty = 1
full = 3
size = 3
colors = 3
init =[[], [0, 1, 1], [2, 0, 1], [0, 2, 2]]
```

Each block represents a different test case with the following parameters:
- `empty`: Number of empty tubes.
- `full`: Number of full tubes.
- `size`: Size of each tube.
- `colors`: Number of different colors.
- `init`: Initial state of the tubes.

## Results

The results of solving the instances will be saved in `finel_result.xlsx` with the following columns:
- `Case Number`: The test case number.
- `Steps Number`: The number of steps taken to solve the puzzle.
- `Runtime (s)`: The time taken to solve the puzzle.

## Detailed Project Description

Refer to `Project_Specifications.pdf` for a detailed description of the project requirements and specifications in Hebrew.
```

This `README.md` file now includes a detailed explanation of the heuristic function used in the A* algorithm.
