from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps
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

@app.route('/story', methods=["POST"])
def addmember():
   imgUrl = request.form['imgUrl']
   storyTitle = request.form['storyTitle']
   storyContent = request.form['storyContent']
   doc = {
      'imgUrl' : imgUrl,
      'storyTitle' : storyTitle,
      'storyContent' : storyContent
   }
   db.myteam.insert_one(doc)
   print(imgUrl, storyContent, storyTitle)

   return jsonify({"msg" : "보내기 성공"})

@app.route('/story', methods=["GET"])
def getStory():
   myStories = list(db.myteam.find({}))
   # print(myStories)
   docs = []
   for story in myStories:
      # print(story)
      doc = {
         'id' : story['_id'],
         'imgUrl': story['imgUrl'],
         'storyTitle' : story['storyTitle'],
         'storyContent': story['storyContent']
      }
      docs.append(doc)

   # print('docs = ', docs)
      
   return dumps(docs)

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)