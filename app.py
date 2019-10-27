from flask import Flask

# set up application referencing the file
app = Flask(__name__)

# set up index route
@app.route('/')
def index():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
