import pandas as pd
from surprise import SVD, Reader, Dataset


class Recommender():
    def __init__(self, ratings_path: str, books_path: str):
        self.ratings_data = pd.read_csv(ratings_path)
        self.books = pd.read_csv(books_path)
        self.data = pd.merge(self.ratings_data, self.books, on='book_id')
        self.predictions = self.renew_predictions()

    def get_all_users(self):
        user_ids = self.ratings_data['user_id'].tolist()
        return list(set(user_ids))

    def get_book_by_id(self, book_id):
        id_df = self.books.loc[self.books['book_id'] == book_id]
        return id_df.values.tolist()[0]

    def renew_predictions(self):
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(self.data[['user_id', 'book_id', 'rating']], reader)
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
        user_df = self.data.loc[self.data['user_id'] == user_id]
        return user_df.values.tolist()




if __name__ == '__main__':
    r_path, b_path = "./Dataset/dataset/cleaner_ratings.csv", "./Dataset/dataset/clean_books.csv"
    new_recommender = Recommender(r_path, b_path)
    prediction_values = new_recommender.get_predictions_by_user(1)
    print(prediction_values)
    new_recommender.get_all_users()
    # print(new_recommender.get_ratings_by_user(1))

# print predictions
# for book_id, _ in get_top_n(uid, predictions):
# #     print(books[books.book_id == book_id]['title'])