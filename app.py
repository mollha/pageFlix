from flask import Flask, render_template, request, jsonify, redirect
from random import choice
from Recommender import Recommender

print('Intializing Recommender...')
app = Flask(__name__)
recommender = Recommender()
print('Complete!\n')

@app.route('/')
def index():
    recommender.get_new_user_id()
    return redirect('/login')

# set up index route
@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/checkuser', methods=['POST'])
def checkUser():
    user_id = request.form['userID'].strip()
    try:
        user_id = int(user_id)
        all_users = recommender.get_all_users()
        if user_id in all_users:
            return 'Success'
        return ''
    except ValueError as e:
        return ''

@app.route('/allbooks', methods=['GET'])
def allBooks():
    book_ids = recommender.get_all_books()
    return jsonify(book_ids)

# @app.route('/createuser', methods=['POST'])
# def createUser():
#     users = recommender.get_all_users()
#     userID = request.form['userID'].strip()
#     if userID in users:
#         return 'False'
#     users.append(userID)
#     return 'True'

@app.route('/getnewid', methods=['GET'])
def getNewUserName():
    return str(recommender.get_new_user_id())

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/welcome')
def view():
    user_id_str = request.args.get('user')
    try:
        user_id = int(user_id_str.strip())
        all_users = recommender.get_all_users()
        if user_id in all_users:
            return render_template('recommendations.html', name=user_id_str)
        return redirect("/login", code=302)
    except Exception as e:
        return redirect("/login", code=302)

# This should do something better with the received data
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    if name:
        newName = name[::-1]
        # , jsonify({'name': newName})
    return " "

@app.route('/getalluserratings', methods=['GET'])
def getUserRatings():
    user_id = request.args.get('user_id')  # get user id as string
    users_ratings = recommender.get_ratings_by_user(int(user_id))
    return jsonify(users_ratings)

@app.route('/getuser', methods=['GET'])
def getUser():
    users = recommender.get_all_users()
    return str(choice(users))

@app.route('/randombook', methods=['GET'])
def getRandomBook():
    user_id = request.args.get('user_id')
    book = recommender.get_unrated_book(int(user_id))
    avg_rating = '{:<04}'.format(book[7])
    genres = book[6].split('|')
    if len(genres) > 3:
        genres = ', '.join(genres[0:3])
    else:
        genres = ', '.join(genres)
    return jsonify(id=book[0], title=book[3], year=book[2], authors=book[1], genres=genres, image_path=book[5], avg_rating=avg_rating)


@app.route('/getbook', methods=['GET'])
def get_book():
    book_id = request.args.get('book_id')   # get book id as string
    user_id = request.args.get('user_id')   # get user id as string
    book = recommender.get_book_by_id(int(book_id))    # get book details from id
    avg_rating = '{:<04}'.format(book[7])
    users_ratings = recommender.get_ratings_by_user(int(user_id))
    rating = ''

    for x in users_ratings:
        if str(x[0][0]) == book_id:
            rating = str(x[1])

    genres = book[6].split('|')
    if len(genres) > 3:
        genres = ', '.join(genres[0:3])
    else:
        genres = ', '.join(genres)
    return jsonify(title=book[3], year=book[2], authors=book[1],
                   genres=genres, image_path=book[5], avg_rating=avg_rating, rating=rating)

@app.route('/getpredictions', methods=['GET'])
def get_predictions():
    user_id = request.args.get('user_id')  # get user id as string
    number = request.args.get('number')
    _, predictions = recommender.get_predictions_by_user(int(user_id), int(number))
    return jsonify(predictions)


@app.route('/deleterating', methods=['POST'])
def delete_rating():
    book_id = request.args.get('book_id')  # get book id as string
    user_id = request.args.get('user_id')  # get user id as string
    recommender.delete_rating(user_id, book_id)
    return ''

@app.route('/updaterating', methods=['POST'])
def update_rating():
    rating = request.form['rating']
    try:
        rating = int(rating)
    except ValueError as e:
        return 'Rating must be a number from 1 to 5'

    if rating > 5 or rating < 1:
        return 'Rating must be a number from 1 to 5'
    # if the rating is not a number, return 'not valid'

    return ''


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=False)
    app.run(debug=True)
