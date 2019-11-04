import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

ratings = pd.read_csv("./Dataset/movie/ratings.csv")
movies = pd.read_csv("./Dataset/movie/movies.csv")
movie_data = pd.merge(ratings, movies, on='movieId')

user_movie_rating = movie_data.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

R = user_movie_rating.values
user_ratings_mean = np.mean(R, axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)
U, sigma, Vt = svds(R_demeaned, k=50)
sigma = np.diag(sigma)
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
preds_df = pd.DataFrame(all_user_predicted_ratings, columns = user_movie_rating.columns)
print(preds_df)

def recommend_movies(predictions_df, userID, movies_df, original_ratings_df, num_recommendations=5):
    user_row_number = userID - 1    #user_id starts at 1
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    user_data = original_ratings_df[original_ratings_df.userId == (userID)]
    user_full = (user_data.merge(movies_df, how='left', left_on='movieId', right_on='movieId').sort_values(['rating'], ascending=False))
    print('User {0} has already rated {1} movies.'.format(userID, user_full.shape[0]))
    print('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))

    # Recommend the highest predicted rating movies that the user hasn't seen yet.
    recommendations = (movies_df[~movies_df['movieId'].isin(user_full['movieId'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
               left_on='movieId', right_on='movieId'). rename(columns={user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending=False).iloc[:num_recommendations, :-1])
    return user_full, recommendations

already_rated, predictions = recommend_movies(preds_df, 2, movies, ratings, 10)
print(already_rated)
print(predictions)
#
# print(movie_data[0:10])
# print(user_movie_rating)
#
# forrest_gump_ratings = user_movie_rating['Forrest Gump (1994)']
# print(forrest_gump_ratings)
#
# print('------------------------')

#movies_like_forest_gump = user_movie_rating.corrwith(forrest_gump_ratings)

# corr_forrest_gump = pd.DataFrame(movies_like_forest_gump, columns=['Correlation'])
# corr_forrest_gump.dropna(inplace=True)
# corr_forrest_gump.sort_values('Correlation', ascending=False).head(10)
# print(corr_forrest_gump.head())



# # Cool additional feature
# Number_movie_ratings = movie_data.groupby('title')['rating'].count().sort_values(ascending=False).head()
# Average_movie_rating = movie_data.groupby('title')['rating'].mean().sort_values(ascending=False).head()
# print(Average_movie_rating)
# print(Number_movie_ratings)
#
# ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())
# ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())
# print(ratings_mean_count.head())