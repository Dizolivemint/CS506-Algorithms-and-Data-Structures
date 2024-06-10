def insertion_sort(arr):
    n = len(arr)
    for index in range(1, n):
        value = arr[index]
        dec_index = index - 1
        # Move elements of arr[0..index-1], that are greater than value,
        # to one position ahead of their current position
        while dec_index >= 0 and value < arr[dec_index]:
            arr[dec_index + 1] = arr[dec_index]
            dec_index -= 1
            print("Pass", index, ":", arr)
        arr[dec_index + 1] = value
        print("Pass", index, ":", arr)
    return arr

# Example usage:
array = [64, 25, 12, 22, 11]
sorted_array = insertion_sort(array)
print("Sorted array:", sorted_array)
