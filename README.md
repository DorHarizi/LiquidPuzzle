Here's a `README.md` file for your project:

```markdown
# Liquid Puzzle Solver

This project provides a solver for the Liquid Puzzle game, where the objective is to sort liquids of different colors into separate tubes. The solver uses the A* algorithm to find the solution efficiently.

## Project Structure

- `LiquidPuzzle.py`: Contains the main implementation of the Liquid Puzzle solver, including the A* algorithm, the `ColorSortPuzzle` class, and the `PriorityQueue` class.
- `instances.txt`: Input file containing various test cases for the Liquid Puzzle solver.
- `finel_result.xlsx`: Output file with the results of the solver's execution on the instances.
- `test.py`: Script for testing the solver with the provided instances.
- `מטלה.pdf`: Detailed description of the project requirements and specifications in Hebrew.

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

Refer to `מטלה.pdf` for a detailed description of the project requirements and specifications in Hebrew.
```

This `README.md` file provides a comprehensive overview of the project, including how to run the solver, dependencies, an explanation of the algorithm, usage instructions, and an example of the input format.
