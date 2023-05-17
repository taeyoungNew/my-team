from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps, ObjectId
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
   myStories = objectIdDecoder(list(db.myteam.find({})))
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

def objectIdDecoder(list):
  results=[]
  for document in list:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results

@app.route('/delete', methods=["DELETE"])
def deleteStory():
   id = ObjectId(request.form['storyId'])
   print('id = ', id)
   db.myteam.delete_one({"_id": ObjectId(id)})
   return jsonify({"msg" : "카드가 삭제되었습니다."})

@app.route('/update', methods=["PUT"])
def updateStory():
   # imgUrl = request.form['newImgUrl']
   contentId = request.form['id']
   title = request.form['newTitle']
   content = request.form['newContent']

   doc = {
      'contentId' : ObjectId(contentId),
      'title' : title,
      'content' : content
   }
   print("doc", doc['contentId'])


   db.myteam.update_one({"_id": ObjectId(contentId)}, {'$set': {'storyTitle' : title, 'storyContent' : content}})

   return jsonify({"msg" : "수정되었습니다."})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)