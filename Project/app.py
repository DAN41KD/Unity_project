from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result')
def game():
    return render_template("result.html")

if __name__ == '__main__':
  app.run(debug=True)