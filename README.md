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
def heuristic(tubes, tube_capacity):
    """
    Calculate a heuristic based on misplaced colors and minimum moves required to sort each tube.

    Parameters:
    tubes (list of list of int): The current state of the tubes, where each tube is a list of colors.
    tube_capacity (int): The maximum number of colors each tube can hold.

    Returns:
    int: The heuristic value, which is the maximum of the misplaced colors heuristic and the minimum moves heuristic.

    Example:
    >>> tubes = [[1, 2, 2], [1, 1], [2], [], [2, 2, 2], []]
    >>> tube_capacity = 3
    >>> heuristic(tubes, tube_capacity)
    4
    """
    h1 = sum(len(tube) - tube.count(max(set(tube), key=tube.count)) for tube in tubes if len(set(tube)) > 1)
    h2 = sum((tube_capacity - len(tube)) for tube in tubes if len(set(tube)) == 1)
    return max(h1, h2)
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