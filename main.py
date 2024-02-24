from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello'

@app.route('/health')
def health():
    return 'Bharat'

if __name__ == '__main__':
    app.run(debug=True)

