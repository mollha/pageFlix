import pandas as pd
from numpy import mean, diag, dot
from scipy.sparse.linalg import svds

ratings_list = [i.strip().split("::") for i in open('./Dataset/movie/ratings.csv', 'r').readlines()]
users_list = [i.strip().split("::") for i in open('/users/nickbecker/Downloads/ml-1m/users.dat', 'r').readlines()]
movies_list = [i.strip().split("::") for i in open('/users/nickbecker/Downloads/ml-1m/movies.dat', 'r').readlines()]
ratings_data = pd.read_csv('./Dataset/movie/ratings.csv')
movie_names = pd.read_csv('./Dataset/movie/movies.csv')
movie_data = pd.merge(ratings_data, movie_names, on='movieId')
structured_data = movie_data.pivot(index="userId", columns="movieId", values='rating').fillna(0)

# de-mean the data to normalize by each users mean
movies = structured_data.as_matrix()
user_ratings_mean = mean(movies, axis=1)
movies_demeaned = movies - user_ratings_mean.reshape(-1, 1)

U, sigma, vt = svds(movies_demeaned, k=50)
sigma = diag(sigma)

all_user_predicted_ratings = dot(dot(U, sigma), vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns=structured_data.columns)

# My equivalent
# -------------------
# rating_values = pd.read_csv('./Dataset/ratings.csv')
# book_names = pd.read_csv('./Dataset/books.csv')
# combined_data = pd.merge(ratings_values, books_names, on='bookID')


# combined_data.pivot(index="userId", columns="movieId", values='rating').fillna(0)


def recommend_books(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    # Get and sort the user's predictions
    user_row_number = userID - 1  # UserID starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)