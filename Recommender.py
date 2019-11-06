import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

# ------------------- Read and Combine Data Sets ------------------
ratings = pd.read_csv("./Dataset/dataset/clean_ratings.csv")
books = pd.read_csv("./Dataset/dataset/clean_books.csv")
book_data = pd.merge(ratings, books, on='book_id')  # Combine the ratings and books tables to form one table
# -----------------------------------------------------------------

# Pivot the table and collate the values
user_book_rating = book_data.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)
rating_values = user_book_rating.values

# Calculate user means and remove them from data to normalize
user_ratings_mean = np.mean(rating_values, axis=1)
R_demeaned = rating_values - user_ratings_mean.reshape(-1, 1)

U, sigma, Vt = svds(R_demeaned, k=min(R_demeaned.shape)-1)
sigma = np.diag(sigma)
all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
pred_dataframe = pd.DataFrame(all_user_predicted_ratings, columns=user_book_rating.columns)

def recommend_books(predictions_df, user_id, books_df, original_ratings_df, num_recommendations=5):
    user_row_number = user_id - 1    #user_id starts at 1
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)
    user_data = original_ratings_df[original_ratings_df.user_id == (user_id)]
    user_full = (user_data.merge(books_df, how='left', left_on='book_id', right_on='book_id').sort_values(['rating'], ascending=False))
    print('User {0} has already rated {1} books.'.format(user_id, user_full.shape[0]))
    print(user_full['title'])
    print('Recommending the highest {0} predicted ratings books not already rated.'.format(num_recommendations))

    # Recommend the highest predicted rating books that the user hasn't seen yet.
    recommendations = (books_df[~books_df['book_id'].isin(user_full['book_id'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
               left_on='book_id', right_on='book_id'). rename(columns={user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending=False).iloc[:num_recommendations, :-1])
    return user_full, recommendations

already_rated, predictions = recommend_books(pred_dataframe, 1, books, ratings, 10)
print(predictions['title'])
#
# print(book_data[0:10])
# print(user_book_rating)
#
# forrest_gump_ratings = user_book_rating['Forrest Gump (1994)']
# print(forrest_gump_ratings)
#
# print('------------------------')

#books_like_forest_gump = user_book_rating.corrwith(forrest_gump_ratings)

# corr_forrest_gump = pd.DataFrame(books_like_forest_gump, columns=['Correlation'])
# corr_forrest_gump.dropna(inplace=True)
# corr_forrest_gump.sort_values('Correlation', ascending=False).head(10)
# print(corr_forrest_gump.head())



# # Cool additional feature
# Number_movie_ratings = book_data.groupby('title')['rating'].count().sort_values(ascending=False).head()
# Average_movie_rating = book_data.groupby('title')['rating'].mean().sort_values(ascending=False).head()
# print(Average_movie_rating)
# print(Number_movie_ratings)
#
# ratings_mean_count = pd.DataFrame(book_data.groupby('title')['rating'].mean())
# ratings_mean_count['rating_counts'] = pd.DataFrame(book_data.groupby('title')['rating'].count())
# print(ratings_mean_count.head())