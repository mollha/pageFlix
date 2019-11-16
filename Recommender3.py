import numpy as np
import pandas as pd


data = pd.read_csv("./Dataset/dataset/clean_ratings.csv", dtype='int32')
book_data = pd.read_csv("./Dataset/dataset/clean_books.csv")
book_data = book_data[['book_id', 'title', 'genres']]

print(book_data.head())

# Create the ratings matrix
ratings_mat = np.ndarray(
    shape=(np.max(data.book_id.values), np.max(data.user_id.values)),
    dtype=np.uint8)
ratings_mat[data.book_id.values-1, data.user_id.values-1] = data.rating.values
normalised_mat = ratings_mat - np.asarray([(np.mean(ratings_mat, 1))]).T
A = normalised_mat.T / np.sqrt(ratings_mat.shape[0] - 1)
U, S, V = np.linalg.svd(A)

def top_cosine_similarity(data, book_id, top_n=10):
    index = book_id - 1 # Movie id starts from 1
    book_row = data[index, :]
    print(book_row)
    magnitude = np.sqrt(np.einsum('ij, ij -> i', data, data))
    similarity = np.dot(book_row, data.T) / (magnitude[index] * magnitude)
    sort_indexes = np.argsort(-similarity)
    return sort_indexes[:top_n]

# Helper function to print top N similar movies
def print_similar_movies(book_data, book_id, top_indexes):
    print('Recommendations for {0}: \n'.format(
    book_data[book_data.book_id == book_id].title.values[0]))
    for id in top_indexes + 1:
        print(book_data[book_data.book_id == id].title.values[0])

k = 50
user_id = 18 # Grab an id from movies.dat
top_n = 10

sliced = V.T[:, :k] # representative data
indexes = top_cosine_similarity(sliced, user_id, top_n)
print_similar_movies(book_data, user_id, indexes)

