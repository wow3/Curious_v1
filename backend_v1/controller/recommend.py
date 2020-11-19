# controller.recommend

from flask import Blueprint, make_response, request, jsonify
from module.collection import Collection
from module.history import History
from module.user import User
from module.question import Question
from module.answer import Answer
import random

recommend = Blueprint('recommend', __name__)

'''
问题10个分类
dict['type'] += score
'''


'''
para: username
返回问题推荐
response: id, title, description, view_count, answer_count, collect_count, gmt_create
'''
@recommend.route('/getrecommend', methods=['GET'])
def get_recommend():
    question = Question()
    user = User()
    answer = Answer()
    collection = Collection()
    history = History()

    username = request.args.get('username')
    idu = user.find_by_username(username=username)[0].id

    dict = {}
    dict['campus'] = 0
    dict['focus'] = 0
    dict['finance'] = 0
    dict['technology'] = 0
    dict['culture'] = 0
    dict['education'] = 0
    dict['depth'] = 0
    dict['entertain'] = 0
    dict['fashion'] = 0
    dict['sports'] = 0

    w1 = 1  # 浏览权重
    w2 = 3  # 回答权重
    w3 = 5  # 收藏权重

    '''
    1.遍历该用户的所有浏览记录，为分类+1
    2.遍历该用户的所有回答记录，为分类+3
    3.遍历该用户的所有收藏记录，为分类+5
    '''

    # 遍历history，为分类赋权重
    res1 = history.find_by_idu(idu=idu)
    for item in res1:
        idq = item.idq
        q = question.find_by_id(id=idq)
        cate = str(q.category)
        dict[cate] += w1

    # 遍历answer
    res2 = answer.find_by_idu(idu=idu)
    for item in res2:
        idq = item.idq
        q = question.find_by_id(id=idq)
        cate = str(q.category)
        dict[cate] += w2

    # 遍历collection
    res3 = collection.find_by_idu(idu=idu)
    for item in res3:
        idq = item.idq
        q = question.find_by_id(id=idq)
        cate = str(q.category)
        dict[cate] += w3

    # 对权重进行排序
    rec = sorted(dict.items(), key=lambda item:item[1], reverse=True)

    # 获取三个类别
    cate_0 = rec[0][0]
    cate_1 = rec[1][0]
    cate_2 = rec[2][0]

    data = []
    list = []
    list.extend(question.find_by_category(category=cate_0))
    list.extend(question.find_by_category(category=cate_1))
    list.extend(question.find_by_category(category=cate_2))

    for item in list:
        q = {}
        q['id'] = item.id
        q['title'] = item.title
        q['category'] = item.category
        q['description'] = item.description
        q['view_count'] = item.view_count
        q['answer_count'] = item.answer_count
        q['collect_count'] = item.collect_count
        q['gmt_create'] = item.gmt_create

        data.append(q)
    random.shuffle(data)
    return jsonify({'data': data})





