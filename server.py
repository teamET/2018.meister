from flask import Flask
from numba import jit

app=Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@jit(nogil=True)
def run():
    app.run(debug=True,host='0.0.0.0',port=8080)

if __name__ == '__main__':
    run()
