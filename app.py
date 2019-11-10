from flask import Flask, render_template, request, jsonify, redirect
from random import choice
from Recommender import Recommender

# set up application referencing the file
app = Flask(__name__)

# recommender = Recommender("./Dataset/dataset/clean_ratings.csv", "./Dataset/dataset/clean_books.csv")
#users = recommender.get_users()
users = ['mol', 'matt']

@app.route('/')
def index():
    return redirect('/login')

# set up index route
@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/signup')
def signup():
    print('hi')
    return render_template('signup.html')

@app.route('/checkuser', methods=['POST'])
def checkUser():
    user_id = request.form['userID'].strip()
    print(user_id)
    if user_id in users:
        return 'True'
    return ''

@app.route('/createuser', methods=['POST'])
def createUser():
    userID = request.form['userID'].strip()
    if userID in users:
        return 'False'
    users.append(userID)
    print('Users', users)
    return 'True'

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
    return choice(users)

@app.route('/getbook', methods=['GET'])
def get_book():
    book_title = request.args.get('book_name')
    # need to get book from its title
    book_title = 'example'.title()

    return jsonify(title=book_title,
                   year='2000',
                   authors='molly',
                   genres='Horror',
                   image_path='https://images.gr-assets.com/books/1303390735m/960.jpg')


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
    app.run(debug=True)
