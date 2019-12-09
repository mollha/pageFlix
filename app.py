from flask import Flask, render_template, request, jsonify, redirect
from random import choice
from RecommenderReset import Recommender

app = Flask(__name__)

# set up application referencing the file
recommender = Recommender("./Dataset/dataset/cleaner_ratings.csv", "./Dataset/dataset/clean_books.csv")
print('Finished intializing Recommender\n')

@app.route('/')
def index():
    return redirect('/login')

# set up index route
@app.route('/login')
def login():
    return render_template('index.html')

# set up recommendations viewing route
@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/checkuser', methods=['POST'])
def checkUser():
    user_id = request.form['userID'].strip()
    if user_id in users:
        return 'True'
    return ''

@app.route('/allbooks', methods=['GET'])
def allBooks():
    book_ids = recommender.get_all_books()
    return jsonify(book_ids)

@app.route('/createuser', methods=['POST'])
def createUser():
    users = recommender.get_all_users()
    userID = request.form['userID'].strip()
    if userID in users:
        return 'False'
    users.append(userID)
    return 'True'

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/welcome')
def view():
    return render_template('recommender_view.html')
# This should do something better with the received data
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    if name:
        newName = name[::-1]
        # , jsonify({'name': newName})
    return render_template("recommender_view.html")

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
    return jsonify(title=book[3], year=book[2], authors=book[1], genres=genres, image_path=book[5], avg_rating=avg_rating)


@app.route('/getbook', methods=['GET'])
def get_book():
    book_id = request.args.get('book_id')
    user_id = request.args.get('user_id')
    book = recommender.get_book_by_id(int(book_id))
    avg_rating = '{:<04}'.format(book[7])
    users_ratings = recommender.get_ratings_by_user(int(user_id))
    rating = ''
    for x in users_ratings:
        if x[0][0] == book_id:
            rating = str(x[0][1])

    genres = book[6].split('|')
    if len(genres) > 3:
        genres = ', '.join(genres[0:3])
    else:
        genres = ', '.join(genres)
    return jsonify(title=book[3], year=book[2], authors=book[1],
                   genres=genres, image_path=book[5], avg_rating=avg_rating, rating=rating)


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
    app.run(debug=True, use_reloader=False)
