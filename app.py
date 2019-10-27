from flask import Flask, render_template, request, jsonify

# set up application referencing the file
app = Flask(__name__)

# set up index route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    email = request.form['email']
    name = request.form['name']

    if email and name:
        newName = name[::-1]
        return jsonify({'name': newName})
    else:
        return jsonify({'error': 'Missing data!'})

# template inheritance


if __name__ == "__main__":
    app.run(debug=True)
