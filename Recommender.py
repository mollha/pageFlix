import pandas as pd
import numpy as np
from scipy.linalg import svd


class Recommender:
    def __init__(self, ratings_path, books_path):
        self.ratings = pd.read_csv(ratings_path)
        self.books = pd.read_csv(books_path)
        self.book_data = pd.merge(self.ratings, self.books, on='book_id')
        self.dataframe = self.book_data.pivot(index='user_id', columns='book_id', values='rating').fillna(0)
        self.predictions_dataframe = None

        self.update_predictions()
        self.delete_user(1)
        self.update_predictions()


    def delete_user(self, user_id: int):
        """
        Delete all ratings belonging to a specific user
        :param user_id: the user to be deleted
        :return: returns NoneType
        """
        #print(self.dataframe.head())
        self.dataframe = self.dataframe.drop(labels=user_id, axis=0)
        #print(self.dataframe.head())


    def get_users(self):
        """
        Get a list containing all valid user_ids
        :return: returns a list of existing user_ids
        """
        return [str(x) for x in self.ratings['user_id'].unique()]

    def edit_ratings(self, user_id: int, rating_dict: dict):
        """
        Add new ratings to the dataset
        :param user_id: an int representing the user_id for the new ratings
        :param rating_dict: a dictionary of book_id : rating, allows more than one updates at a time
        :return: NoneType
        """
        for book_id in rating_dict:
            self.dataframe.at[user_id, int(book_id)] = rating_dict[int(book_id)]

    def update_predictions(self):
        rating_values = self.dataframe.values
        user_ratings_mean = np.mean(rating_values, axis=1)
        r_demeaned = rating_values - user_ratings_mean.reshape(-1, 1)
        # Singular Value Decomposition on ratings
        u, sigma, vt = svd(r_demeaned, full_matrices=False)
        sigma = np.diag(sigma)
        all_user_predicted_ratings = np.dot(np.dot(u, sigma), vt) + user_ratings_mean.reshape(-1, 1)
        self.predictions_dataframe = pd.DataFrame(all_user_predicted_ratings, columns=self.dataframe.columns)


    def get_recommendations(self, user_id: int, num_recommendations: int):
        user_row_number = list(self.dataframe.index).index(user_id)
        sorted_user_predictions = self.predictions_dataframe.iloc[user_row_number].sort_values(ascending=False)
        user_data = self.ratings[self.ratings['user_id'] == user_id]
        already_rated = (user_data.merge(self.books, how='left', left_on='book_id', right_on='book_id').
                         sort_values(['rating'], ascending=False))
        recommendations = (self.books[~self.books['book_id'].isin(already_rated['book_id'])].
                           merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                           left_on='book_id', right_on='book_id').
                           rename(columns={user_row_number: 'Predictions'}).
                           sort_values('Predictions', ascending=False)
                           .iloc[:num_recommendations, :-1])
        return already_rated, recommendations