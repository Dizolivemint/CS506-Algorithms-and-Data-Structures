import heapq

def a_star_search_stream(distance_matrix, start_city=0):
    num_cities = len(distance_matrix)
    heap = []
    
    # Heuristic function: estimate the cost to complete the tour by returning to the start city
    def heuristic(current_city):
        return min(distance_matrix[current_city][i] for i in range(num_cities) if i != current_city)

    # Initial state: (f(n), g(n), [current_path])
    initial_state = (heuristic(start_city), 0, [start_city])
    heapq.heappush(heap, initial_state)
    
    best_route = None
    best_distance = float('inf')
    generation = 0  # Start generation counter

    while heap:
        generation += 1
        current_f, current_g, current_path = heapq.heappop(heap)
        current_city = current_path[-1]
        
        if len(current_path) == num_cities:
            # Complete the tour by returning to the start_city
            total_cost = current_g + distance_matrix[current_city][start_city]
            if total_cost < best_distance:
                best_distance = total_cost
                best_route = current_path + [start_city]
                yield {
                    'generation': generation,
                    'route': best_route,
                    'distance': best_distance,
                    'fitness': 1 / best_distance if best_distance > 0 else float('inf')
                }
            continue
        
        for next_city in range(num_cities):
            if next_city not in current_path:
                new_g = current_g + distance_matrix[current_city][next_city]
                new_f = new_g + heuristic(next_city)
                heapq.heappush(heap, (new_f, new_g, current_path + [next_city]))

    if best_route:
        # Final best result
        yield {
            'generation': generation,
            'route': best_route,
            'distance': best_distance,
            'fitness': 1 / best_distance if best_distance > 0 else float('inf')
        }
