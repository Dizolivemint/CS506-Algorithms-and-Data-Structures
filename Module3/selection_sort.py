def selection_sort(arr):
    num_iterations = len(arr)
    for index in range(num_iterations):
        # Assume the minimum is the first element
        min_index = index
        # Iterate over the unsorted elements
        for unsorted_index in range(index + 1, num_iterations):
            if arr[unsorted_index] < arr[min_index]:
                min_index = unsorted_index
        # Swap the found minimum element with the first element
        arr[index], arr[min_index] = arr[min_index], arr[index]
        print("Pass", index + 1, ":", arr)
    return arr

# Example usage:
array = [64, 25, 12, 22, 11]
sorted_array = selection_sort(array)
print("Sorted array:", sorted_array)
