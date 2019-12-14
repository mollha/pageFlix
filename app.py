from flask import Flask, render_template, request, jsonify, redirect, json
from random import choice
from Recommender import Recommender

print('Intializing Recommender...')
app = Flask(__name__, template_folder='templates')
recommender = Recommender()
print('Complete!\n')

# -------------------------------- CONFIGURE TEMPLATE ROUTES -------------------------------
@app.route('/')
def login():
    """
    Configure route to login / home page - from here you can log in as an existing user
    :return: Render login page
    """
    return render_template('index.html')


@app.route('/signup')
def signup():
    """
    Configure route to sign up - from here you can sign up as a new user with a suggested user id
    :return: Render sign up page
    """
    return render_template('signup.html')


@app.route('/faq')
def faq():
    """
    Configure route to FAQs page - provides extra instruction on how to use the system
    :return: Render FAQs page
    """
    return render_template('faq.html')


@app.route('/welcome')
def view():
    """
    Configure route to dashboard - here, you can update ratings and view recommendations
    :return: Render welcome page / dashboard
    """
    user_id_str = request.args.get('user')
    try:
        user_id = int(user_id_str.strip())
        all_users = recommender.get_all_users()
        if user_id in all_users:        # render user dashboard if a valid user id is provided
            return render_template('recommendations.html', name=user_id_str)
        return redirect("/")       # if user id is invalid, redirect to the login page
    except AttributeError:
        return redirect("/")       # if no user id is provided, redirect to the login page

# ------------------------------ CONFIGURE POST REQUEST ENDPOINTS ---------------------------
@app.route('/checkuser', methods=['POST'])
def check_user():
    """
    Check that a user id is valid (i.e. the user exists)
    :return: A boolean value indicating whether or not the user ID provided is valid
    """
    user_id = request.form['userID'].strip()
    try:
        user_id = int(user_id)
        all_users = recommender.get_all_users()
        if user_id in all_users:        # if the user id is valid, return True
            return json.dumps(True)
        return json.dumps(False)        # if the user id is not valid, return False
    except ValueError:
        return json.dumps(False)        # return False if there is a ValueError


@app.route('/createuser', methods=['POST'])
def create_user():
    """
    Create new user in recommender when a user id is provided
    :return: Dummy response
    """
    user_id = request.form['user_id'].strip()
    recommender.create_user(int(user_id))
    recommender.get_all_users()
    return ''


@app.route('/deleterating', methods=['POST'])
def delete_rating():
    """
    Delete rating of specific book by a specific user
    :return: return a dummy response
    """
    book_id = request.form['book_id'].strip()  # get book id as string
    user_id = request.form['user_id'].strip() # get user id as string
    recommender.delete_rating(int(user_id), int(book_id))
    return ''


@app.route('/updaterating', methods=['POST'])
def update_rating():
    """
    Submit an updated rating for a previously rated book, or a new rating for an unrated book
    :return:
    """
    # TODO will need editing for full functionality
    rating = request.form['rating']
    book_id = request.form['book_id']  # get book id as string
    user_id = request.form['user_id']  # get user id as string
    try:
        rating = int(rating)
    except ValueError:
        return 'Rating must be a number from 1 to 5'

    if rating > 5 or rating < 1:
        return 'Rating must be a number from 1 to 5'
    recommender.update_rating(int(user_id), int(book_id), rating)
    return ''

# ------------------------------ CONFIGURE GET REQUEST ENDPOINTS ---------------------------
@app.route('/allbooks', methods=['GET'])
def all_books():
    """
    Get a list of all books in the system
    :return: return list of books
    """
    book_ids = recommender.get_all_books()
    return jsonify(book_ids)


@app.route('/getnewid', methods=['GET'])
def get_new_user_name():
    """
    Get a new, valid user id from the recommender
    :return: return new, valid user id as a string
    """
    return str(recommender.get_new_user_id())


@app.route('/getalluserratings', methods=['GET'])
def get_user_ratings():
    """
    Get all ratings from a specific user
    :return: return a list of all ratings from a specific user
    """
    user_id = request.args.get('user_id')  # get user id as string
    users_ratings = recommender.get_ratings_by_user(int(user_id))
    users_ratings.sort(key=lambda x: x[0][3])
    return jsonify(users_ratings)


@app.route('/getuser', methods=['GET'])
def get_user():
    """
    Get a random valid user id
    :return: return the user id
    """
    users = recommender.get_all_users()
    return str(choice(users))


@app.route('/randombook', methods=['GET'])
def get_random_book():
    """
    Get a random unrated book
    If all books have been rated, return a random rated book
    :return: return random book as JSON
    """
    user_id = request.args.get('user_id')
    book = recommender.get_unrated_book(int(user_id))
    # TODO, need to deal with the eventuality where all books have been rated
    # I believe I have dealt with this in the recommender, however, need to test
    avg_rating = '{:<04}'.format(book[7])
    genres = book[6].split('|')
    if len(genres) > 3:
        genres = ', '.join(genres[0:3])
    else:
        genres = ', '.join(genres)
    return jsonify(id=book[0], title=book[3], year=book[2], authors=book[1],
                   genres=genres, image_path=book[5], avg_rating=avg_rating)


@app.route('/getbook', methods=['GET'])
def get_book():
    """
    Get a specific book that the user has requested to view
    :return: Book details as JSON
    """
    book_id = request.args.get('book_id')   # get book id as string
    user_id = request.args.get('user_id')   # get user id as string
    book = recommender.get_book_by_id(int(book_id))    # get book details from id
    avg_rating = '{:<04}'.format(book[7])
    users_ratings = recommender.get_ratings_by_user(int(user_id))
    rating = ''
    for x in users_ratings:     # get user rating if one already exists
        if str(x[0][0]) == book_id:
            rating = str(x[1])

    genres = book[6].split('|')
    if len(genres) > 3:
        genres = ', '.join(genres[0:3])
    else:
        genres = ', '.join(genres)
    return jsonify(id=book[0], title=book[3], year=book[2], authors=book[1],
                   genres=genres, image_path=book[5], avg_rating=avg_rating, rating=rating)


@app.route('/getpredictions', methods=['GET'])
def get_predictions():
    """
    Get either 5 or 10 user-specific predictions
    :return:
    """
    # TODO, see what happens to the predictions when all books rated
    user_id = request.args.get('user_id')  # get user id as string
    number = request.args.get('number')  # get number of requested predictions
    _, predictions = recommender.get_predictions_by_user(int(user_id), int(number))
    return jsonify(predictions)


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=False)
    # TODO disable reloader on submission
    app.run(debug=False)
