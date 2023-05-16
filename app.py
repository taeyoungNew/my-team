from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.iijkbtz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/taeyoung')
def memberpage():
   return render_template('taeyoung.html')


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)