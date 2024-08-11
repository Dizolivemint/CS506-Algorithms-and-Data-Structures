import heapq

def best_first_search_stream(distance_matrix, start_city=0):
    num_cities = len(distance_matrix)
    visited = set()
    heap = []
    
    # Initial state: starting from the start_city with path containing only the start_city and zero cost
    initial_state = (0, [start_city])
    heapq.heappush(heap, initial_state)
    
    best_route = None
    best_distance = float('inf')
    generation = 0  # Start generation counter

    while heap:
        generation += 1
        current_cost, current_path = heapq.heappop(heap)
        current_city = current_path[-1]
        
        if len(current_path) == num_cities:
            # Complete the tour by returning to the start_city
            total_cost = current_cost + distance_matrix[current_city][start_city]
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
                new_cost = current_cost + distance_matrix[current_city][next_city]
                heapq.heappush(heap, (new_cost, current_path + [next_city]))

    if best_route:
        # Final best result
        yield {
            'generation': generation,
            'route': best_route,
            'distance': best_distance,
            'fitness': 1 / best_distance if best_distance > 0 else float('inf')
        }
