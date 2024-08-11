from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from genetic_algorithm.genetic_algorithm import genetic_algorithm
from best_first_search.best_first_search_stream import best_first_search_stream
import io
import time
import itertools
import os

app = Flask(__name__)
CORS(app)

def convert_to_serializable(obj):
    """ Helper function to convert numpy types to native Python types recursively. """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(i) for i in obj]
    return obj

def stream_solutions(distance_matrix, pop_size, mutation_rate, crossover_rate, use_pmx, use_ox, use_elitism, fitness_threshold, no_improvement_generations, use_aco, pheromone_threshold, use_sa, sa_initial_temp, sa_cooling_rate, sa_num_iterations):
    def generate():
        start_time = time.time()

        for solution in genetic_algorithm(
            distance_matrix, 
            pop_size=pop_size, 
            mutation_rate=mutation_rate, 
            crossover_rate=crossover_rate, 
            use_pmx=use_pmx, 
            use_ox=use_ox, 
            use_elitism=use_elitism,
            fitness_threshold=fitness_threshold,
            no_improvement_generations=no_improvement_generations,
            use_aco=use_aco,
            pheromone_threshold=pheromone_threshold,
            use_sa=use_sa,
            sa_cooling_rate=sa_cooling_rate,
            sa_initial_temp=sa_initial_temp,
            sa_num_iterations=sa_num_iterations
        ):
            serializable_solution = {k: convert_to_serializable(v) for k, v in solution.items()}
            yield f"data: {json.dumps(serializable_solution)}\n\n"
        
        end_time = time.time()  # End time
        total_time = end_time - start_time  # Calculate total time
        
        # Yield the total time at the end of the event stream
        yield f"data: {json.dumps({'total_time': total_time})}\n\n"
        
    return Response(generate(), mimetype='text/event-stream')

@app.route('/run-ga', methods=['POST'])
def run_ga():
    data = request.form.to_dict()
    file = request.files['file']
    df = pd.read_csv(io.StringIO(file.read().decode('utf-8')), index_col=0)
    
    # Debugging: Print the dataframe to verify contents
    print(df.head())

    # Drop the first column (city names)
    df = df.drop(columns=df.columns[0])

    distance_matrix = df.to_numpy()
    
    # Debugging: Print the numpy array and its dtype
    print(distance_matrix)
    print(distance_matrix.dtype)
    
    distance_matrix = distance_matrix.astype(float) / 1000  # Convert distances from meters to kilometers
    
    if np.any(np.isnan(distance_matrix)) or np.any(distance_matrix < 0):
        return "Distance matrix contains invalid values.", 400
    
    np.fill_diagonal(distance_matrix, 0)
    if np.any((distance_matrix == 0) & (np.eye(len(distance_matrix)) == 0)):
        return "Distance matrix contains zero values off the diagonal.", 400

    pop_size = int(data.get('pop_size', 100))
    mutation_rate = float(data.get('mutation_rate', 0.01))
    crossover_rate = float(data.get('crossover_rate', 0.7))
    use_pmx = data.get('use_pmx', 'false').lower() == 'true'
    use_ox = data.get('use_ox', 'false').lower() == 'true'
    use_elitism = data.get('use_elitism', 'false').lower() == 'true'
    fitness_threshold = float(data.get('fitness_threshold')) if data.get('fitness_threshold') else None
    no_improvement_generations = int(data.get('no_improvement_generations', 20))
    use_aco = data.get('use_aco', 'false').lower() == 'true'
    pheromone_threshold = float(data.get('pheromone_threshold', 5))
    use_sa = data.get('use_sa', 'false').lower() == 'true'
    sa_initial_temp = float(data.get('sa_initial_temp', 1000))
    sa_cooling_rate = float(data.get('sa_cooling_rate', 0.995))
    sa_num_iterations = int(data.get('sa_num_iterations', 1000))

    return stream_solutions(distance_matrix, pop_size, mutation_rate, crossover_rate, use_pmx, use_ox, use_elitism, fitness_threshold, no_improvement_generations, use_aco, pheromone_threshold, use_sa, sa_initial_temp, sa_cooling_rate, sa_num_iterations)

@app.route('/stream-solutions', methods=['GET'])
def stream_solutions_endpoint():
    # This function should be implemented if you need a separate endpoint for streaming solutions
    return Response("Not implemented", status=501)

@app.route('/brute', methods=['GET'])
def brute_force_tsp():
    # Assuming the distance matrix is passed as a query parameter
    distance_matrix = request.args.get('distance_matrix')
    if not distance_matrix:
        return "Missing distance matrix", 400

    distance_matrix = np.array(json.loads(distance_matrix))

    def find_best_brute_force_solution(distance_matrix):
        num_cities = len(distance_matrix)
        cities = list(range(num_cities))
        
        start_time = time.time()
        best_route = None
        best_distance = float('inf')
        
        for permutation in itertools.permutations(cities):
            # Ensuring the route starts and ends with the first city
            if permutation[0] != 0:
                continue
            route = list(permutation) + [permutation[0]]
            distance = sum(distance_matrix[route[i], route[i + 1]] for i in range(num_cities))

            if distance < best_distance:
                best_distance = distance
                best_route = route
        
        end_time = time.time()
        total_time = end_time - start_time

        return {
            'final_best_route': best_route,
            'final_best_distance': best_distance / 1000,
            'total_time': total_time
        }

    # Get the best solution
    best_solution = find_best_brute_force_solution(distance_matrix)
    
    # Convert to serializable format
    serializable_solution = convert_to_serializable(best_solution)
    
    return jsonify(serializable_solution)

@app.route('/best-first-search', methods=['GET'])
def run_best_first_search():
    # Decode the distance matrix from the query string
    distance_matrix_str = request.args.get('distance_matrix')
    
    if not distance_matrix_str:
        return "Missing distance matrix", 400
    
    try:
        # Decode the string to a list of lists
        distance_matrix = np.array(json.loads(distance_matrix_str)).astype(float)
    except (ValueError, TypeError) as e:
        return f"Invalid distance matrix format: {str(e)}", 400
    
    # Convert distances from meters to kilometers
    distance_matrix /= 1000
    
    if np.any(np.isnan(distance_matrix)) or np.any(distance_matrix < 0):
        return "Distance matrix contains invalid values.", 400
    
    np.fill_diagonal(distance_matrix, 0)
    if np.any((distance_matrix == 0) & (np.eye(len(distance_matrix)) == 0)):
        return "Distance matrix contains zero values off the diagonal.", 400

    # Optional start_city parameter with a default of 0
    start_city = int(request.args.get('start_city', 0))
    
    def generate():
        start_time = time.time()
        
        for result in best_first_search_stream(distance_matrix, start_city):
            serializable_result = convert_to_serializable(result)
            yield f"data: {json.dumps(serializable_result)}\n\n"
        
        end_time = time.time()
        total_time = end_time - start_time
        yield f"data: {json.dumps({'total_time': total_time})}\n\n"

    return Response(generate(), mimetype='text/event-stream')
  
if __name__ == '__main__':
    # Check if the app is running on Render
    render = os.environ.get("RENDER", False)
    if render:
        # Running on Render, use the provided PORT
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
    else:
        # Running locally
        app.run(port=5000)
