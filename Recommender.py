import pandas as pd


ratings_data = pd.read_csv('./Dataset/movie/ratings.csv')
movie_names = pd.read_csv('./Dataset/movie/movies.csv')
movie_data = pd.merge(ratings_data, movie_names, on='movieId')
