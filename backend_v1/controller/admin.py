# controller.admin

from flask import Blueprint, make_response, request, jsonify
from module.user import User
from module.notification import Notification

admin = Blueprint('admin', __name__)


'''
para: 
获取用户列表
response: id, username, nickname, gmt_create, banned
'''
@admin.route('/getuserlist', methods=['GET'])
def get_user_list():
    user = User()
    res = user.find_all()
    data = []
    for item in res:
        u = {}
        u['id'] = item.id
        u['username'] = item.username
        u['nickname'] = item.nickname
        u['gmt_create'] = item.gmt_create
        u['banned'] = item.banned
        data.append(u)
    return jsonify({'data': data})


'''
para: 
获取未处理的举报信息
respnse: id, content, gmt_create
'''
@admin.route('/gettipoff', methods=['GET'])
def get_tipoff():
    notification = Notification()
    res = notification.find_tip0()
    data = []
    for item in res:
        tip = {}
        tip['id'] = item.id
        tip['content'] = item.content
        tip['gmt_create'] = item.gmt_create
        data.append(tip)
    return jsonify({'data': data })


'''
para: username
封禁用户
response: success or fail
'''
@admin.route('/banuser', methods=['POST'])
def ban_user():
    user = User()
    username = request.form.get('username')
    flag = user.do_ban(username=username)
    if flag == 1:
        return 'success'
    else:
        return 'fail'


'''
para: username
解禁用户
response: success or fail
'''
@admin.route('/unban', methods=['POST'])
def unban():
    user = User()
    username = request.form.get('username')
    flag = user.unban(username=username)
    if flag == 1:
        return 'success'
    else:
        return 'fail'