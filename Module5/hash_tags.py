import numpy as np

# Example pre-trained embeddings (usually you would load these from a model)
embeddings = {
    "tech": np.array([0.1, 0.2, 0.3]),
    "technology": np.array([0.1, 0.2, 0.29]),
    "computer": np.array([0.11, 0.2, 0.3]),  # Similar to "tech" and "technology
    "sports": np.array([0.4, 0.5, 0.6]),
    "football": np.array([0.41, 0.5, 0.61]),
    "basketball": np.array([0.4, 0.51, 0.6]),
    "soccer": np.array([0.41, 0.5, 0.61])
}

def get_embedding(tag):
    # Retrieve the embedding vector for a given tag
    return embeddings.get(tag, np.zeros(3))  # Default to a zero vector if the tag is not found

class CosineHashTable:
    def __init__(self, size):
        # Initialize the hash table with the given size
        self.size = size
        self.table = [[] for _ in range(size)]  # Create an empty list for each bucket

    def _cosine_similarity(self, vec1, vec2):
        # Compute the cosine similarity between two vectors
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    def _hash_function(self, tag):
        # Compute the hash index for a given tag using the sum of the embedding vector components
        vector = get_embedding(tag)  # Get the embedding vector for the tag
        vector_sum = np.sum(vector)  # Sum the components of the vector
        return int(vector_sum * 1000) % self.size  # Compute the index by taking the modulus

    def insert(self, tag):
        # Insert a tag into the hash table
        index = self._hash_function(tag)  # Compute the index for the tag
        self.table[index].append(tag)  # Append the tag to the bucket

    def get_similar_tags(self, tag):
        # Retrieve similar tags from the hash table
        index = self._hash_function(tag)  # Compute the index for the tag
        similar_tags = []
        original_vector = get_embedding(tag)
        for stored_tag in self.table[index]:
            stored_vector = get_embedding(stored_tag)
            if self._cosine_similarity(original_vector, stored_vector) <= .99:  # Adjust similarity threshold as needed
                similar_tags.append(stored_tag)
        return similar_tags

# Example usage
cosine_table = CosineHashTable(10)  # Create a hash table with 10 buckets
tags = embeddings.keys()

# Insert tags into the hash table
for tag in tags:
    cosine_table.insert(tag)

# Retrieve and print similar tags for a given tag
print(cosine_table.get_similar_tags("tech")) 
print(cosine_table.get_similar_tags("sports"))