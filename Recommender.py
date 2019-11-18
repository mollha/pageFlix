import pandas as pd
from surprise import SVD, Reader, Dataset


class Recommender:
    def __init__(self, ratings_path: str, books_path: str):
        print('Initializing Recommender...')
        self.ratings = pd.read_csv(ratings_path)
        self.books = pd.read_csv(books_path)
        self.predictions = self.renew_predictions()

    def update_rating(self, user_id, book_id, rating):
        # self.data.loc[(self.data['user_id'] == user_id) & (self.data['book_id'] == book_id)] = [user_id, book_id, rating]
        pass

    def get_unrated_book(self, user_id: int):
        user_rated_books = self.get_ratings_by_user(user_id)
        user_rated_book_ids = [x[0][0] for x in user_rated_books]

        while True:
            random_book_id = self.books['book_id'].sample(n=1).tolist()[0]
            if random_book_id not in user_rated_book_ids:
                return self.get_book_by_id(random_book_id)


    def delete_user(self, user_id: str):
        """
        Delete a user by removing every rating they have created
        :param user_id: a str representing the user_id of the user to be removed
        :return: None
        """
        # Modify the ratings dataframe to contain every rating NOT made by user_id
        self.ratings = self.ratings[self.ratings.user_id != user_id]

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
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(all_data[['user_id', 'book_id', 'rating']], reader)
        train_set = data.build_full_trainset()
        svd = SVD()
        svd.fit(train_set)
        test_set = train_set.build_anti_testset()
        return svd.test(test_set)       # return predictions

    def get_predictions_by_user(self, user_id: int, n=10):
        top_n = []
        for uid, iid, true_r, est, _ in self.predictions:
            if uid == user_id:
                top_n.append((iid, est))
        sorted_predictions = sorted(top_n, key=lambda est: est[1], reverse=True)[0:n]
        return [self.get_book_by_id(b_id) for b_id, _ in sorted_predictions]

    def get_ratings_by_user(self, user_id: int):
        user_df = self.ratings.loc[self.ratings['user_id'] == user_id].values.tolist()
        return [(self.get_book_by_id(x[1]), x[2]) for x in user_df]




# if __name__ == '__main__':
#     r_path, b_path = "./Dataset/dataset/cleaner_ratings.csv", "./Dataset/dataset/clean_books.csv"
#     new_recommender = Recommender(r_path, b_path)
#     prediction_values = new_recommender.get_predictions_by_user(1)

    # print(new_recommender.get_ratings_by_user(1))

# print predictions
# for book_id, _ in get_top_n(uid, predictions):
# #     print(books[books.book_id == book_id]['title'])