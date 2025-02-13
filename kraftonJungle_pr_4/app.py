from flask import Flask, render_template, jsonify, request

import requests

from bson import ObjectId

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.KJ_pr4

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/postMemo', methods=['POST'])
def postMemo():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    memo = {'title': title_receive,
            'content': content_receive,
            'like': 0 }
    db.memos.insert_one(memo)
    return jsonify({'result': 'success'})

@app.route('/readMemo', methods=['GET'])
def readMemo():
    items = db.memos.find({}).sort({'like': -1})
    result = []
    for item in items :
        memo = {
            'id': str(item['_id']),
            'title': item['title'],
            'content': item['content'],
            'like': item['like']
        }
        result.append(memo)
    return jsonify({'result': 'success', 'memos': result})

@app.route('/deleteMemo', methods=['POST'])
def deleteMemo():
    id_receive = request.form['id_give']
    db.memos.delete_one({'_id': ObjectId(id_receive)})
    
    return jsonify({'result': 'success'})

@app.route('/likeMemo', methods=['POST'])
def likeMemo():
    id_receive = request.form['id_give']
    like = db.memos.find_one({'_id':ObjectId(id_receive)})
    updatedLike = like['like'] + 1
    db.memos.update_one({'_id': ObjectId(id_receive)}, {'$set':{'like': updatedLike}})
    
    return jsonify({'result': 'success'})

@app.route('/updateMemo', methods=['POST'])
def updateMemo():
    id_receive = request.form['id_give']
    new_title_receive = request.form['new_title_give']
    new_content_receive = request.form['new_content_give']
    db.memos.update_one({'_id': ObjectId(id_receive)}, {'$set':{'title': new_title_receive, 'content': new_content_receive}})

    return jsonify({'result': 'success'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5004, debug=True)