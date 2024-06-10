import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

class ArrayVisualizer:
    def __init__(self, array, keys):
        self.array = array
        self.size = len(array)
        self.width = 800
        self.height = 600
        self.bar_width = self.width // self.size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.keys = keys
        self.total_draw_time = 0

    def draw_bars(self, array, color_array):
        start_time = time.perf_counter()
        self.screen.fill((0, 0, 0))
        max_value = max(array, key=lambda x: x[self.keys[0]])[self.keys[0]]
        for i in range(self.size):
            x = i * self.bar_width
            y = self.height - (array[i][self.keys[0]] / max_value * self.height)
            color = color_array[i]
            pygame.draw.rect(self.screen, color, (x, y, self.bar_width, self.height - y))
        pygame.display.flip()
        end_time = time.perf_counter()
        self.total_draw_time += (end_time - start_time)

    def animate(self, generator):
        clock = pygame.time.Clock()
        sorting_start_time = time.perf_counter()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            try:
                array, color_array = next(generator)
                self.draw_bars(array, color_array)
                clock.tick(60)
            except StopIteration:
                running = False

        sorting_end_time = time.perf_counter()
        
        total_sorting_time = sorting_end_time - sorting_start_time - self.total_draw_time
        return total_sorting_time

def bubble_sort(array, keys, visualizer):
    def bubble_sort_generator():
        n = len(array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if (array[j][keys[0]], array[j][keys[1]]) > (array[j + 1][keys[0]], array[j + 1][keys[1]]):
                    array[j], array[j + 1] = array[j + 1], array[j]
                color_array = [(255, 0, 0) if x == j or x == j + 1 else (0, 0, 255) for x in range(len(array))]
                yield array, color_array
            color_array = [(0, 0, 255) for _ in range(len(array))]
            yield array, color_array

    return visualizer.animate(bubble_sort_generator())
        
def merge_sort(array, keys, visualizer):
    def merge_sort_generator(array, left, right):
        if left < right:
            middle = (left + right) // 2
            yield from merge_sort_generator(array, left, middle)
            yield from merge_sort_generator(array, middle + 1, right)
            yield from merge(array, left, middle, right)

    def merge(array, left, middle, right):
        left_half = array[left:middle + 1]
        right_half = array[middle + 1:right + 1]
        left_index = right_index = 0
        merged_index = left

        while left_index < len(left_half) and right_index < len(right_half):
            if (left_half[left_index][keys[0]], left_half[left_index][keys[1]]) <= (right_half[right_index][keys[0]], right_half[right_index][keys[1]]):
                array[merged_index] = left_half[left_index]
                left_index += 1
            else:
                array[merged_index] = right_half[right_index]
                right_index += 1
            merged_index += 1
            color_array = [(255, 0, 0) if x == merged_index else (0, 0, 255) for x in range(len(array))]
            yield array, color_array

        while left_index < len(left_half):
            array[merged_index] = left_half[left_index]
            left_index += 1
            merged_index += 1
            color_array = [(255, 0, 0) if x == merged_index else (0, 0, 255) for x in range(len(array))]
            yield array, color_array

        while right_index < len(right_half):
            array[merged_index] = right_half[right_index]
            right_index += 1
            merged_index += 1
            color_array = [(255, 0, 0) if x == merged_index else (0, 0, 255) for x in range(len(array))]
            yield array, color_array

    return visualizer.animate(merge_sort_generator(array, 0, len(array) - 1))

def create_shuffled_patient_records(size):
    names = [f'Patient {i}' for i in range(size)]
    random.shuffle(names)
    return [{"name": names[i], "age": random.randint(21, 30), "height": random.randint(100, 120)} for i in range(size)]

array_size = 20
keys_to_sort_by = ['age', 'height']

# Create and shuffle the patient records
shuffled_array = create_shuffled_patient_records(array_size)

# Merge Sort Visualization
print("Visualizing Merge Sort")
visualizer = ArrayVisualizer(shuffled_array.copy(), keys_to_sort_by)

# Sort the shuffled array using Bubble Sort
new_array = shuffled_array.copy()
sorting_time = bubble_sort(new_array, keys_to_sort_by, visualizer)
total_sorting_time_array = [sorting_time]

# Sort the shuffled array using Merge Sort
new_array = shuffled_array.copy()
sorting_time = merge_sort(new_array, keys_to_sort_by, visualizer)
total_sorting_time_array.append(sorting_time)

print('Array after sorting:')
for record in new_array:
    print(record)

print('Total sorting time for Bubble Sort:', total_sorting_time_array[0])
print('Total sorting time for Merge Sort:', total_sorting_time_array[1])
pygame.quit()
sys.exit()