# controller.question
import hashlib
import re

from flask import Blueprint, make_response, request, jsonify
from module.question import Question

question = Blueprint('question', __name__)

'''
para: username, title, category, description
提交问题接口
update: question
'''
@question.route('/addquestion', methods=['POST'])
def add():
    question = Question()
    username = request.form.get('username').strip()
    title = request.form.get('title').strip()
    category = request.form.get('category').strip()
    description = request.form.get('description').strip()

    res = question.add_question(username=username, title=title, category=category, description=description)

    if res == 1:
        return 'add-success'
    else:
        return 'add-error'

'''
para: category
返回问题接口(全部)
response: id, title, description, view_count, answer_count, collect_count, gmt_create
'''
@question.route('/home/question', methods=['GET'])
def get_by_category():
    question = Question()
    category = request.args.get("category")
    data = []
    res = question.find_by_category('category').all()
    for item in res:
        q = {}
        q['id'] = item.id
        q['title'] = item.title
        q['description'] = item.description
        q['view_count'] = item.view_count
        q['answer_count'] = item.answer_count
        q['collect_count'] = item.collect_count
        q['gmt_create'] = item.gmt_create

        data.append(q)
    return jsonify({'data': data})

'''
para: category, page
返回问题接口(分页)
response: id, title, description, view_count, ansewr_count, ccollect_count, gmt_create
'''
@question.route('/getquestion', methods=['GET'])
def get_by_category_limit():
    question = Question()
    category = request.args.get("category")
    print('category=' + category)
    page = request.args.get('page')
    print('page=' + page)
    data = []
    res = question.find_limit_by_category(category=category, page=page, count=5)    # 数据太少，暂且返回5
    for item in res:
        q = {}
        q['id'] = item.id
        q['title'] = item.title
        q['description'] = item.description
        q['view_count'] = item.view_count
        q['answer_count'] = item.answer_count
        q['collect_count'] = item.collect_count
        q['gmt_create'] = item.gmt_create

        data.append(q)
    return jsonify({'data': data})

'''
para: 
返回blank问题
response: id, title, description, view_count, ccollect_count, gmt_create
'''
@question.route('/getquestionb', methods=['GET'])
def get_question_blank():
    question = Question()
    data = []
    res = question.find_all_blank()
    for item in res:
        q = {}
        q['id'] = item.id
        q['title'] = item.title
        q['description'] = item.description
        q['view_count'] = item.view_count
        q['collect_count'] = item.collect_count
        q['gmt_create'] = item.gmt_create

        data.append(q)
    return jsonify({'data': data})


'''
para: key
查找带有关键字的问题
'''
@question.route('/search', methods=['GET'])
def do_search():
    question = Question()
    key = request.args.get('key')
    data = []
    res = question.find_by_searchkey(key=key)
    for item in res:
        q = {}
        q['id'] = item.id
        q['title'] = item.title
        q['category'] = item.category
        q['description'] = item.description
        q['view_count'] = item.view_count
        q['collect_count'] = item.collect_count
        q['answer_count'] = item.answer_count
        q['gmt_create'] = item.gmt_create

        data.append(q)
    return jsonify({'data': data})




'''
para: idq
question表中收藏数+1
update: question
'''
@question.route('/addqacc', methods=['GET'])
def addcc():
    question = Question()
    idq = request.args.get("idq")
    question.add_collect_count(idq=idq)
    return 'add-success'
