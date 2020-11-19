# controller.history

from flask import Blueprint, make_response, request, jsonify
from module.question import Question
from module.user import User
from module.history import History

history = Blueprint('history', __name__)


'''
para: username, idq 
新增历史记录
update: question, history
'''
@history.route('/addhistory', methods=['POST'])
def add_history():
    history = History()
    user = User()
    question = Question()
    # 获取请求中的参数
    username = request.form.get("username")
    idq = request.form.get("idq")
    # 根据用户名获取id
    idu = user.find_by_username(username)[0].id
    # 更新表question和history
    question.add_view_count(idq=idq)
    history.add(idu=idu, idq=idq)
    return 'pass'


'''
para: username 
查询用户的历史记录
response: idq, title
'''
@history.route('/gethistory', methods=['GET'])
def get_history():
    history = History()
    user = User()
    question = Question()

    username = request.args.get("username")
    idu = user.find_by_username(username)[0].id
    res = history.find_by_idu(idu=idu)
    data=[]
    for item in res:
        col = {}
        idq = item.idq
        title = question.find_by_id(id=idq).title
        col['idq'] = idq
        col['title'] = title

        data.append(col)
    return jsonify({'data': data})