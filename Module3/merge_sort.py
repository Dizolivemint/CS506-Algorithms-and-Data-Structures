def merge_sort(array):
    if len(array) > 1:
        middle_index = len(array) // 2  # Find the middle of the array
        left_half = array[:middle_index]  # Divide the array into two halves
        right_half = array[middle_index:]

        # Recursively sort both halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Merge the sorted halves
        left_index = right_index = merged_index = 0

        # Copy data to temp arrays left_half[] and right_half[]
        while left_index < len(left_half) and right_index < len(right_half):
            if left_half[left_index] < right_half[right_index]:
                array[merged_index] = left_half[left_index]
                left_index += 1
            else:
                array[merged_index] = right_half[right_index]
                right_index += 1
            merged_index += 1

        # Checking if any element was left in the left_half
        while left_index < len(left_half):
            array[merged_index] = left_half[left_index]
            left_index += 1
            merged_index += 1

        # Checking if any element was left in the right_half
        while right_index < len(right_half):
            array[merged_index] = right_half[right_index]
            right_index += 1
            merged_index += 1

        print(f"Merged: {array}")

# Example usage:
array = [64, 25, 12, 22, 11]
print("Original array:", array)
merge_sort(array)
print("Sorted array:", array)