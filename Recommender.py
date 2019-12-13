import pandas as pd
import numpy as np
from random import randint
from scipy.sparse.linalg import svds


class Recommender:
    def __init__(self, ratings_path, books_path):
        # connection = sqlite3.connect('databasename.db')
        # cursor = connection.cursor()

        self.ratings = pd.read_csv(ratings_path)
        # self.ratings = pd.read_sql_query("SELECT * FROM Ratings", connection)
        self.books = pd.read_csv(books_path)
        # self.books = pd.read_sql_query("SELECT * FROM Books", connection)
        self.predictions = self.renew_predictions()
        #print(self.get_predictions_by_user(1, 1))

    def get_unrated_book(self, user_id: int):
        user_rated_books = self.get_ratings_by_user(user_id)
        user_rated_book_ids = [x[0][0] for x in user_rated_books]

        while True:
            random_book_id = self.books['book_id'].sample(n=1).tolist()[0]
            if random_book_id not in user_rated_book_ids:
                return self.get_book_by_id(random_book_id)

    def get_random_id(self) -> str:

        def verify_new(new_id: int) -> bool:
            self.get_ratings_by_user(new_id)
            pass

        def generate(k: int) -> str:
            output = []
            while k < len(output):
                random_num = randint(0, 10)
                output.append(str(random_num))
            return "".join(output)


    def delete_rating(self, user_id: str, book_id: str):
        """
        Deletes a rating given the book_id and the user_id of the user who gave it
        Searches for all rows that do not contain the rating
        :param user_id: str representing the user_id of the author of the rating
        :param book_id: str representing the book_id of the rated book
        :return: None
        """
        # Modifies the ratings dataframe
        self.ratings = self.ratings[(self.ratings.user_id != user_id) | (self.ratings.book_id != book_id)]
        self.predictions = self.renew_predictions()

    def delete_user(self, user_id: str):
        """
        Delete a user by removing every rating they have created
        :param user_id: a str representing the user_id of the user to be removed
        :return: None
        """
        # Modify the ratings dataframe to contain every rating NOT made by user_id
        self.ratings = self.ratings[self.ratings.user_id != user_id]

    def get_mean_rating(self, book_id: str):
        """
        Calculates the mean rating of a book to 2 decimal places
        :param book_id: a str representing the book_id of the book
        :return: Mean rating (float) or a string indicating that no such book has been rated
        """
        all_book_ratings = self.ratings.loc[self.ratings['book_id'] == book_id]
        if len(all_book_ratings):
            return round(all_book_ratings['rating'].astype(int).mean(axis=0), 2)
        return 'N/A'    # return a string which indicates the book has no ratings

    def get_all_users(self):
        """
        Gets a list containing the user_ids of every user by extracting unique user_ids from ratings
        :return: a list containing all existing user_ids
        """
        user_ids = self.ratings['user_id'].tolist()
        return list(set(user_ids))

    def get_all_books(self):
        book_ids = self.books['book_id'].tolist()
        return [self.get_book_by_id(x) for x in book_ids]

    def get_ratings_by_user(self, user_id: int):
        user_df = self.ratings.loc[self.ratings['user_id'] == user_id].values.tolist()
        return [(self.get_book_by_id(x[1]), x[2]) for x in user_df]

    def check_user(self):
        pass

    # def edit_ratings(self, user_id: int, rating_dict: dict):
    #     """
    #     Add new ratings to the dataset
    #     :param user_id: an int representing the user_id for the new ratings
    #     :param rating_dict: a dictionary of book_id : rating, allows more than one updates at a time
    #     :return: NoneType
    #     """
    #     for book_id in rating_dict:
    #         self.dataframe.at[user_id, int(book_id)] = rating_dict[int(book_id)]

    def get_book_by_id(self, book_id):
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

    def renew_predictions(self):
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

    def get_predictions_by_user(self, user_id: int, num_recommendations: int):
        sorted_user_predictions = self.predictions.iloc[user_id - 1].sort_values(ascending=False)
        user_data = self.ratings[self.ratings.user_id == user_id]
        already_rated = (user_data.merge(self.books, how='left', left_on='book_id', right_on='book_id').
                         sort_values(['rating'], ascending=False))
        recommendations = (self.books[~self.books['book_id'].isin(already_rated['book_id'])].
                           merge(pd.DataFrame(sorted_user_predictions).reset_index(), how='left',
                           left_on='book_id', right_on='book_id'). rename(columns={user_id - 1: 'Predictions'}).
                           sort_values('Predictions', ascending=False).iloc[:num_recommendations, :-1])
        return already_rated, recommendations.values.tolist()


if __name__ == "__main__":
    recommender = Recommender("./Dataset/dataset/cleaner_ratings.csv", "./Dataset/dataset/clean_books.csv")