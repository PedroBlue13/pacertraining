from flask import Flask

app = Flask (__name__)


@app.route('/')
def home():
    return 'Hello'

@app.route('/sum/<int:a>/<int:b>')
def sum(a,b):
    return str(a + b)


if __name__ == '__main__':
    app.run(debug=True)
