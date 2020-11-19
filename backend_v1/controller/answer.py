# controller.question
import hashlib
import re

from flask import Blueprint, make_response, request, jsonify
from module.answer import Answer
from module.question import Question
from module.user import User

answer = Blueprint('answer', __name__)


'''
para: idq 
根据问题id返回回答
response; id, username, content, upvote, gmt_create 
'''
@answer.route('/getanswer', methods=['GET'])
def get_answers():
    answer = Answer()
    idq = request.args.get("idq")
    data = []

    res = answer.find_by_idq(idq)
    for item in res:
        a = {}
        idu = item.idu
        user = User()
        username = user.find_by_id(idu).username
        avatar_url = user.find_by_id(idu).avatar_url
        a['id'] = item.id
        a['username'] = username
        a['avatar_url'] = '../assets/avatar/'+avatar_url
        a['content'] = item.content
        a['upvote'] = item.upvote
        a['gmt_create'] = item.gmt_create

        data.append(a)
    return jsonify({'data': data})


'''
para: username
根据用户名查询回答
response: id, idq, title, content, upvote, gmt_create
'''
@answer.route('/getmyanswer', methods=['GET'])
def get_my_answer():
    answer = Answer()
    user = User()
    question = Question()
    data = []

    username = request.args.get('username')
    idu = user.find_by_username(username=username)[0].id
    res = answer.find_by_idu(idu=idu)
    for item in res:
        idq = item.idq
        title = question.find_by_id(id=idq).title
        a = {}
        a['id'] = item.id
        a['idq'] = idq
        a['title'] = title
        a['content'] = item.content
        a['upvote'] = item.upvote
        a['gmt_create'] = item.gmt_create

        data.append(a)
    return jsonify({'data': data})


'''
para: username
根据用户名查询回答数量，获赞数量，比率
response: c_answer, c_upvote, ratio, avg_answer, avg_upvote, avg_ratio
'''
@answer.route('/countmyanswer', methods=['GET'])
def count_my_answer():
    answer = Answer()
    user = User()

    username = request.args.get('username')
    idu = user.find_by_username(username=username)[0].id

    data = {}

    c_answer = answer.count_by_idu(idu=idu)
    c_upvote = answer.count_upvote_by_idu(idu=idu)
    ratio = 0
    if c_answer != 0:
        ratio = round(c_upvote/c_answer, 2)


    data['c_answer'] = c_answer
    data['c_upvote'] = c_upvote
    data['ratio'] = ratio

    avg_answer = answer.count_avg()
    avg_upvote = answer.count_avg_upvote()
    avg_ratio = round(avg_upvote/avg_answer, 2)

    data['avg_answer'] = avg_answer
    data['avg_upvote'] = avg_upvote
    data['avg_ratio'] = avg_ratio

    return jsonify({'data': data})




'''
para: username, idq, content 
提交回答
update: question, answer
'''
@answer.route('/addanswer', methods=['POST'])
def add():
    answer = Answer()
    user = User()
    question = Question()
    username = request.form.get('username').strip()
    print(username)
    print(user.find_by_username(username))
    idu = user.find_by_username(username)[0].id     # 根据用户名获取idu

    idq = request.form.get('idq').strip()
    content = request.form.get('content').strip()

    question.add_answer_count(idq)                  # 问题回答数+1

    res = answer.add_answer(idq, idu, content)
    if res == 1:
        return 'add-success'
    else:
        return 'add-error'


    
    
