# controller.collection

from flask import Blueprint, make_response, request, jsonify
from module.question import Question
from module.user import User
from module.collection import Collection

collection = Blueprint('collection', __name__)


'''
para: username, idq 
新增问题收藏记录
update: question, collection
'''
@collection.route('/addcollection', methods=['POST'])
def add_collection():
    collection = Collection()
    user = User()
    question = Question()
    # 获取请求中的参数
    username = request.form.get("username")
    idq = request.form.get("idq")
    # 获取用户id
    idu = user.find_by_username(username)[0].id

    res = collection.find_by_iduidq(idu=idu, idq=idq)
    if len(res) > 0:
        return 'repeated'
    else:
        # 更新两张表question和collection
        question.add_collect_count(idq=idq)  # 问题表收藏数+1
        collection.add(idu=idu, idq=idq)
        return 'success'



'''
para: username 
查询用户的问题收藏
response: idq, title, category, view_count, answer_count, collect_count
'''
@collection.route('/getmycollection', methods=['GET'])
def get_my_collection():
    collection = Collection()
    user = User()
    question = Question()

    username = request.args.get("username")
    idu = user.find_by_username(username)[0].id
    res = collection.find_by_idu(idu=idu)
    data=[]
    for item in res:
        col = {}
        idq = item.idq
        q = question.find_by_id(id=idq)
        title = q.title
        category = q.category
        description = q.description
        view_count = q.view_count
        answer_count = q.answer_count
        collect_count = q.collect_count
        gmt_create = q.gmt_create
        col['idq'] = idq
        col['title'] = title
        col['category'] = category
        col['description'] = description
        col['view_count'] = view_count
        col['collect_count'] = collect_count
        col['answer_count'] = answer_count
        col['gmt_create'] = gmt_create

        data.append(col)
    return jsonify({'data': data})
