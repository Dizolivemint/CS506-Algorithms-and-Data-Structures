import random

def quicksort(array, low, high):
    if low < high:
        # partition_index is partitioning index, array[partition_index] is now at the right place
        partition_index = partition(array, low, high)

        # Print the array after partitioning
        print(f"Partitioned at index {partition_index} with pivot {array[partition_index]}: {array}")

        # Separately sort elements before and after partition
        quicksort(array, low, partition_index - 1)
        quicksort(array, partition_index + 1, high)

def partition(array, low, high):
    pivot_index = median_of_three(array, low, high)
    pivot = array[pivot_index]
    array[pivot_index], array[high] = array[high], array[pivot_index]  # Move pivot to end
    index = low - 1  # Index of smaller element

    for current in range(low, high):
        if array[current] <= pivot:
            index += 1
            array[index], array[current] = array[current], array[index]  # swap

    array[index + 1], array[high] = array[high], array[index + 1]  # swap pivot into the correct place
    return index + 1

def median_of_three(array, low, high):
    mid = (low + high) // 2
    if array[low] > array[mid]:
        array[low], array[mid] = array[mid], array[low]
    if array[low] > array[high]:
        array[low], array[high] = array[high], array[low]
    if array[mid] > array[high]:
        array[mid], array[high] = array[high], array[mid]
    return mid

# Example usage:
array = [64, 25, 12, 22, 11]
print("Original array:", array)
quicksort(array, 0, len(array) - 1)
print("Sorted array:", array)