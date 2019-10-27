from flask import Flask, render_template

# set up application referencing the file
app = Flask(__name__)

# set up index route
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
