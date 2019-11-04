from flask import Flask, render_template, request, jsonify, redirect
from random import choice

# set up application referencing the file
app = Flask(__name__)

users = ['mollcool', 'yaycool', 'yamomisahoe', 'stefan']

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


@app.route('/createuser', methods=['POST'])
def createUser():
    userID = request.form['userID'].strip()
    if userID in users:
        return 'False'
    users.append(userID)
    print('Users', users)
    return 'True'

@app.route('/view')
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

if __name__ == "__main__":
    app.run(debug=True)
