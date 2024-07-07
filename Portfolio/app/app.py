from flask import Flask, request, Response
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
from genetic_algorithm.genetic_algorithm import genetic_algorithm
import io

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

def stream_solutions(distance_matrix, pop_size, mutation_rate, crossover_rate, use_pmx, use_ox, use_elitism, fitness_threshold, no_improvement_generations):
    def generate():
        for solution in genetic_algorithm(
            distance_matrix, 
            pop_size=pop_size, 
            mutation_rate=mutation_rate, 
            crossover_rate=crossover_rate, 
            use_pmx=use_pmx, 
            use_ox=use_ox, 
            use_elitism=use_elitism,
            fitness_threshold=fitness_threshold,
            no_improvement_generations=no_improvement_generations
        ):
            serializable_solution = {k: convert_to_serializable(v) for k, v in solution.items()}
            yield f"data: {json.dumps(serializable_solution)}\n\n"
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

    return stream_solutions(distance_matrix, pop_size, mutation_rate, crossover_rate, use_pmx, use_ox, use_elitism, fitness_threshold, no_improvement_generations)

@app.route('/stream-solutions', methods=['GET'])
def stream_solutions_endpoint():
    # This function should be implemented if you need a separate endpoint for streaming solutions
    return Response("Not implemented", status=501)

if __name__ == '__main__':
    app.run(port=5000)
