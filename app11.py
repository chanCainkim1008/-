from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.8nfmq87.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

#movie쪽 수정해야함
@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({},{'_id':False}))
    return jsonify({'result':all_movies})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)