from flask import Flask, render_template, url_for

# set up application referencing the file
app = Flask(__name__)

# set up index route
@app.route('/')
def index():
    return render_template('index.html')

# template inheritance


if __name__ == "__main__":
    app.run(debug=True)
