from flask import Flask, render_template, request, jsonify
from bson.json_util import dumps, ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb+srv://sparta:test@cluster0.iijkbtz.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

# 방명록 루트
# 유저이름 & 코멘트 저장하기
@app.route('/guestbook', methods=["POST"])
def saveComments():
   guestName = request.form['guestName'];
   commentText = request.form['commentText']
   print(guestName, commentText)
   doc = {
      
      'guestName' : guestName,
      'commentText' : commentText
   }
   succes = db.guestbook.insert_one(doc)
   return jsonify({'msg' : '연결됨'})

# 유저이름 & 코멘트 불러오기
@app.route('/guestbook', methods=["GET"])
def getComments():
   docs = objectIdDecoder(list(db.guestbook.find({})))
   print(docs)

   return jsonify({'rows' : docs})
def objectIdDecoder(list):
  results=[]
  for document in list:
    document['_id'] = str(document['_id'])
    results.append(document)
  return results

# 유저코멘트 지우기
@app.route('/guestbook', methods=["DELETE"])
def deleteCommets():
   print('잘옴')
   commentId = ObjectId(request.form['commentId'])
   db.guestbook.delete_one({"_id": commentId})
   # db.guestbook.delete_one({"_id": ObjectId(id)})
   return jsonify({"msg" : "카드가 삭제되었습니다."})

# 유저코멘트 수정
@app.route('/guestbook', methods=["PUT"])
def updateComment():
   print('updateComment')
   dataId = request.form['id']
   newName = request.form['newName'];
   newComment = request.form['newComment']

   db.guestbook.update_one({"_id": ObjectId(dataId)}, {'$set': {'guestName' : newName, 'commentText' : newComment}})
   return jsonify({'msg' : '수정되었습니다.'})


# 각멤버페이지의 루트
@app.route('/taeyoung')
def taeyoungpage():
   return render_template('taeyoung.html')

@app.route('/heeyeun')
def heeyeunpage():
   print('희윤님 페이지')
   return render_template('heeyeun.html')

@app.route('/hoseok')
def hoseokpage():
   print('호석님 페이지')
   return render_template('hoseok.html')

@app.route('/jeongmi')
def jeongmi():
   print('정미님')
   return render_template('jeongmi.html')

@app.route('/changgeun')
def changgeun():
   print('창근님')
   return render_template('changgeun.html')


# 데이터 저장 처리
# 태영
@app.route('/story', methods=["POST"])
def addTaeyoungStory():
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

   return jsonify({"msg" : "저장 성공"})

# 희윤님 
@app.route('/heeyeunstory', methods=["POST"])
def addHeeYeunStory():
   storyTitle = request.form['storyTitle']
   storyContent = request.form['storyContent']
   doc = {
      'storyTitle' : storyTitle,
      'storyContent' : storyContent
   }
   db.heeyeun.insert_one(doc)
   # print(doc)
   return jsonify({"msg" : "저장 성공"})


# 개인페이지 데이터 가져오기
# 태영
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

# 희윤님
@app.route('/heeyeunstory', methods=["GET"])
def getHeeyuenStory():
   # list(db.fans.find({}, {'_id': False}))
   myStories = list(db.heeyeun.find({}, {'_id': False}))
   print('myStories = ', myStories)
   # docs = []
   # for story in myStories:
   #    # print(story)
   #    doc = {
   #       'storyTitle' : story['storyTitle'],
   #       'storyContent': story['storyContent']
   #    }
   #    docs.append(doc)
   # print('docs = ', docs)
   return myStories 



# 방명록 게스트이름과 댓글 저장
# @app.route('/', methods=["POST"])
# def


# 
# 태영 개인페이지 데이터 삭제
@app.route('/delete', methods=["DELETE"])
def deleteStory():
   id = ObjectId(request.form['storyId'])
   print('id = ', id)
   db.myteam.delete_one({"_id": ObjectId(id)})
   return jsonify({"msg" : "카드가 삭제되었습니다."})


# 태영 개인페이지 데이터 수정
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
   print("doc = ", doc)


   db.myteam.update_one({"_id": ObjectId(contentId)}, {'$set': {'storyTitle' : title, 'storyContent' : content}})

   return jsonify({"msg" : "수정되었습니다."})





if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)