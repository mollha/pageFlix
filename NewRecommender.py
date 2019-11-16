import pandas as pd
from surprise import SVD, Reader, Dataset

ratings_path, books_path = "./Dataset/dataset/cleaner_ratings.csv", "./Dataset/dataset/clean_books.csv"
ratings = pd.read_csv(ratings_path)
books = pd.read_csv(books_path)
books = books[['book_id', 'title', 'genres']]
book_data = pd.merge(ratings, books, on='book_id')

reader = Reader(rating_scale=(1, 5))
print('Loading Data')
data = Dataset.load_from_df(book_data[['user_id', 'book_id', 'rating']], reader)
print('Building training set')
trainset = data.build_full_trainset()
print('Training set built successfully')


def get_top_n(user, predictions, n=10):
    # First map the predictions to each user.
    top_n = []
    for uid, iid, true_r, est, _ in predictions:
        if uid == user:
            top_n.append((iid, est))
    return sorted(top_n, key=lambda est: est[1], reverse=True)[0:n]
    # # Then sort the predictions for each user and retrieve the k highest ones.
    # for uid, user_ratings in top_n.items():
    #     user_ratings.sort(key=lambda x: x[1], reverse=True)
    #     top_n[uid] = user_ratings[:n]
    #
    # return top_n


# Use the famous SVD algorithm.
svd = SVD()
print('Fitting data')
svd.fit(trainset)
print('Fit successful')
print('Building test set')
testset = trainset.build_anti_testset()
print('Making Predictions')
predictions = svd.test(testset)

uid = 1  # raw user id (as in the ratings file). They are **strings**!

print(books.head())
for book_id, _ in get_top_n(uid, predictions):
    print(books[books.book_id == book_id]['title'])
print()
svd.fit(trainset)
predictions = svd.test(testset)

for book_id, _ in get_top_n(uid, predictions):
    print(books[books.book_id == book_id]['title'])