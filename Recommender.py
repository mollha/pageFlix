import pandas as pd
import numpy as np
from random import randint
from scipy.sparse.linalg import svds
import sqlite3


class Recommender:
    def __init__(self):
        """
        Initialise the recommender using the provided database
        """
        connection = sqlite3.connect('Data.db')
        self.ratings = pd.read_sql_query("SELECT * FROM Ratings", connection)
        self.books = pd.read_sql_query("SELECT * FROM Books", connection)
        self.users = self.ratings['user_id'].astype(int)
        self.users.drop_duplicates(keep="first", inplace=True)
        self.users = self.users.reset_index(drop=True)
        self.predictions = self.renew_predictions()

    def get_unrated_book(self, user_id: int) -> list:
        """
        Get a book that the user has not rated, unless they have rated all books, then we return a previously rated book
        :param user_id: int representing the user id
        :return:
        """
        user_rated_books = self.get_ratings_by_user(user_id)
        user_rated_book_ids = [x[0][0] for x in user_rated_books]

        count = 0
        while True:
            random_book_id = self.books['book_id'].sample(n=1).tolist()[0]
            if (random_book_id not in user_rated_book_ids) or count >= len(self.books.index):
                return self.get_book_by_id(random_book_id)
            count += 1

    def delete_rating(self, user_id: int, book_id: int) -> None:
        """
        Deletes a rating given the book_id and the user_id of the user who gave it
        Searches for all rows that do not contain the rating
        :param user_id: str representing the user_id of the author of the rating
        :param book_id: str representing the book_id of the rated book
        :return: None
        """
        self.ratings = self.ratings[(self.ratings.user_id != user_id) | (self.ratings.book_id != book_id)]
        self.predictions = self.renew_predictions()

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by removing every rating they have created
        :param user_id: a str representing the user_id of the user to be removed
        :return: None
        """
        # Modify the ratings dataframe to contain every rating NOT made by user_id
        self.ratings = self.ratings[self.ratings.user_id != user_id]
        self.users = self.users[self.users.user_id != user_id]
        self.predictions = self.renew_predictions()

    def get_mean_rating(self, book_id: str) -> str:
        """
        Calculates the mean rating of a book to 2 decimal places
        :param book_id: a str representing the book_id of the book
        :return: Mean rating (float) or a string indicating that no such book has been rated
        """
        all_book_ratings = self.ratings.loc[self.ratings['book_id'] == book_id]
        if len(all_book_ratings):
            return round(all_book_ratings['rating'].astype(int).mean(axis=0), 2)
        return 'N/A'  # return a string which indicates the book has no ratings

    def get_all_users(self) -> list:
        """
        Gets a list containing the user_ids of every user by extracting unique user_ids from ratings
        :return: a list containing all existing user_ids
        """
        user_ids = self.users.tolist()
        return list(set(user_ids))

    def get_all_books(self) -> list:
        """
        Get a list of all books in dataset
        :return: list of all books
        """
        book_ids = self.books['book_id'].tolist()
        return [self.get_book_by_id(x) for x in book_ids]

    def get_top_rated_books(self, n: int) -> list:
        """
        Get the n top-rated books - used when the user has no current ratings
        :param n: number of books to return
        :return: list of n top-rated books
        """
        all_books = self.get_all_books()
        all_books.sort(key=lambda x: x[7], reverse=True)
        return all_books[0: n]

    def get_ratings_by_user(self, user_id: int) -> list:
        """
        Get user-specific ratings
        :param user_id: the user to retrieve ratings for
        :return: user ratings
        """
        user_df = self.ratings.loc[self.ratings['user_id'] == user_id].values.tolist()
        return [(self.get_book_by_id(x[1]), x[2]) for x in user_df]

    def get_new_user_id(self) -> int:
        """
        Randomly generate a new, valid user-id
        :return: user id as an int
        """
        while True:
            new_id = randint(0, 99999)
            if new_id not in self.users:
                return new_id

    def create_user(self, user_id: int) -> None:
        """
        Create a new user given a valid user id
        :param user_id: user id for the newly created user
        :return: NoneType
        """
        new_row = pd.Series(user_id)
        self.users = self.users.append(new_row, ignore_index=True)

    def update_rating(self, user_id: int, book_id: int, rating: int) -> None:
        """
        Update / create rating
        :param user_id: user providing the rating
        :param book_id: book being rated
        :param rating: value of rating (between 1 and 5 inclusive)
        :return: NoneType
        """
        self.delete_rating(user_id, book_id)
        df = pd.DataFrame({"user_id": user_id, "book_id": book_id, "rating": rating}, index=[0])
        self.ratings = self.ratings.append(df, ignore_index=True)
        self.predictions = self.renew_predictions()

    def get_book_by_id(self, book_id) -> list:
        """
        Return the details of the book corresponding to book_id
        :param book_id: a str representing the book_id of the corresponding book
        :return: list containing book details
        """
        mean_rating = self.get_mean_rating(book_id)
        # Get the row from the books dataframe corresponding to the book_id
        id_df = self.books.loc[self.books['book_id'] == book_id]
        # Return the first, and only, entry in the list as another list
        new_list = id_df.values.tolist()[0]
        new_list.append(str(mean_rating))
        return new_list

    def renew_predictions(self) -> pd.DataFrame:
        all_data = pd.merge(self.ratings, self.books, on='book_id')
        dataframe = all_data.pivot_table(index='user_id', columns='book_id', values='rating').fillna(0)
        rating_values = dataframe.values
        user_ratings_mean = np.mean(rating_values, axis=1)
        r_demeaned = rating_values - user_ratings_mean.reshape(-1, 1)
        # Singular Value Decomposition on ratings
        u, sigma, vt = svds(r_demeaned, k=min(r_demeaned.shape) - 1)
        sigma = np.diag(sigma)
        all_user_predicted_ratings = np.dot(np.dot(u, sigma), vt) + user_ratings_mean.reshape(-1, 1)
        return pd.DataFrame(all_user_predicted_ratings, columns=dataframe.columns)

    def get_predictions_by_user(self, user_id: int, num_recommendations: int) -> tuple:
        try:
            index = self.users[self.users == user_id].index[0]
            sorted_user_predictions = self.predictions.iloc[index].sort_values(ascending=False)
            user_data = self.ratings[self.ratings.user_id == user_id]
            already_rated = (user_data.merge(self.books, how='left', left_on='book_id', right_on='book_id').
                             sort_values(['rating'], ascending=False))
            recommendations = (self.books[~self.books['book_id'].isin(already_rated['book_id'])].
                                   merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                                         left_on='book_id', right_on='book_id').rename(columns={index: 'Predictions'}).
                                   sort_values('Predictions', ascending=False).iloc[:num_recommendations, :-1])
            return already_rated, recommendations.values.tolist()
        except IndexError:
            return pd.DataFrame(columns=["user_id", "rating", "book_id", "authors",
                                         "year", "title", "language_code", "image_url", "genres"]), \
                   self.get_top_rated_books(num_recommendations)


if __name__ == "__main__":
    recommender = Recommender()
