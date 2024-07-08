# CS506-Algorithms-and-Data-Structures 

## Portfolio
# Traveling Salesman Problem (TSP) Solver

This project provides a solution to the Traveling Salesman Problem (TSP) using both brute force and genetic algorithms. It consists of a React frontend and a Python backend.

## Setup and Run

### Backend (Python)

1. Navigate to the `Portfolio` directory.
2. Install the required packages:
   ```
   python -m pip install -r requirements.txt
   ```
3. Run the backend server:
   ```
   python -m app.app
   ```

### Frontend (React)

1. Navigate to the `Portfolio` directory.
2. Install the required packages:
   ```
   npm install
   ```
3. Start the frontend server:
   ```
   npm run start
   ```

## User Options

### Population Size
- **Description**: The number of individuals in the population for each generation in the genetic algorithm.
- **Example**: `100`

### Mutation Rate
- **Description**: The probability that a mutation will occur in an individual. Mutations introduce new genetic material into the population, promoting diversity.
- **Example**: `0.01`

### Crossover Rate
- **Description**: The probability that two individuals will exchange genetic material during crossover. Crossover combines parts of two parent solutions to create new offspring solutions.
- **Example**: `0.7`

### Genetic Algorithm Options

#### Use PMX (Partially Mapped Crossover)
- **Description**: A crossover technique that preserves the order and position of genes from the parent solutions. It helps maintain relative positions of cities in the routes.
- **Example**: `true` or `false`

#### Use OX (Order Crossover)
- **Description**: A crossover technique that ensures the offspring inherit the relative order of cities from the parent solutions. It helps in maintaining valid permutations of cities.
- **Example**: `true` or `false`

#### Use Elitism
- **Description**: A technique where a certain number of the best individuals from the current generation are carried over to the next generation without alteration. This ensures that the best solutions are preserved.
- **Example**: `true` or `false`

### Termination Criteria

#### Fitness Threshold
- **Description**: The algorithm stops if an individual with a fitness value (total route distance) less than or equal to this threshold is found. Lower fitness values indicate better solutions.
- **Example**: `5000`

#### No Improvement Generations
- **Description**: The algorithm stops if there is no improvement in the best solution found for this number of consecutive generations. This helps prevent endless computation when no better solutions are found.
- **Example**: `20`

## How It Works

### Brute Force Method

The brute force method generates all possible permutations of routes and calculates the total distance for each route. It then identifies the route with the shortest distance. This method guarantees finding the optimal solution but is computationally expensive and impractical for large numbers of cities.

### Genetic Algorithm Method

The genetic algorithm is a heuristic method inspired by natural selection. It uses a population of candidate solutions that evolve over generations. Each generation involves selection, crossover, and mutation to produce new offspring. Over time, the population converges towards an optimal or near-optimal solution.

### Backend

The Python backend handles the heavy lifting for the TSP calculations. It includes the implementation of both brute force and genetic algorithms, providing an API to the frontend to request and receive solutions.

### Frontend

The React frontend provides an interactive user interface for inputting TSP parameters and visualizing the solutions. It communicates with the Python backend to fetch solutions and display them to the user in real-time.
