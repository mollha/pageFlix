import pandas as pd
import numpy as np

ratings_list = [i.strip().split("::") for i in open('./Dataset/ml-1m/ratings.dat', 'r').readlines()]
users_list = [i.strip().split("::") for i in open('./Dataset/ml-1m/users.dat', 'r').readlines()]
movies_list = [i.strip().split("::") for i in open('./Dataset/ml-1m/movies.dat', 'r').readlines()]

ratings_df = pd.DataFrame(ratings_list, columns = ['UserID', 'MovieID', 'Rating', 'Timestamp'], dtype = int)
movies_df = pd.DataFrame(movies_list, columns = ['MovieID', 'Title', 'Genres'])
movies_df['MovieID'] = movies_df['MovieID'].apply(pd.to_numeric)

R_df = ratings_df.pivot(index = 'UserID', columns ='MovieID', values = 'Rating').fillna(0)


print(R_df[0:5])

R_df.head()
R = R_df.values
user_ratings_mean = np.mean(R, axis=1)
R_demeaned = R - user_ratings_mean.reshape(-1, 1)


from numpy.linalg import svd
U, sigma, Vt = svds(R_demeaned, k = 50)
sigma = np.diag(sigma)