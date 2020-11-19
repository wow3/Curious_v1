# controller.notification


from flask import Blueprint, make_response, request, jsonify
from module.notification import Notification
from module.user import User
from module.question import Question
from module.answer import Answer

notification = Blueprint('notification', __name__)



'''
para: username
获取已读通知
response: id, content, gmt_create
'''
@notification.route('/getnotification1', methods=['GET'])
def get_notification_1():
    notification = Notification()
    user = User()
    username = request.args.get("username")
    idu = user.find_by_username(username)[0].id
    data=[]
    res = notification.find_by_idu_1(idu=idu)
    for item in res:
        nt = {}
        nt['id'] = item.id
        nt['content'] = item.content
        nt['gmt_create'] = item.gmt_create

        data.append(nt)
    return jsonify({'data': data})


'''
para: username
获取未读通知
response: id, content, gmt_create
'''
@notification.route('/getnotification0', methods=['GET'])
def get_notification_0():
    notification = Notification()
    user = User()
    username = request.args.get("username")
    idu = user.find_by_username(username)[0].id
    data=[]
    res = notification.find_by_idu_0(idu=idu)
    for item in res:
        nt = {}
        nt['id'] = item.id
        nt['content'] = item.content
        nt['gmt_create'] = item.gmt_create

        data.append(nt)
    return jsonify({'data': data})


'''
para: 通知id    
标记某个通知为已读
update: notification
'''
@notification.route('/markasread', methods=['GET'])
def mark_as_read():
    notification = Notification()
    id = request.args.get('id')
    res = notification.isread(id)
    if res == 1:
        return 'mark-success'
    else:
        return 'mark-fail'


'''
para: idq      
问题有新回答事件
update: notification
'''
@notification.route('/newanswer', methods=['GET'])
def new_answer():
    question = Question()
    idu = question.find_by_id().idu     # 查找出问题提出用户

    notification = Notification()
    notification.newanswer(idq, idu)
    return 'success'


'''
para: username, ida   
回答被点赞事件
update: notification
'''
@notification.route('/newupvote', methods=['GET'])
def new_upvote():
    user = User()
    answer = Answer()

    username = request.args.get('username')
    ida = request.args.get('ida')

    idu2 = user.find_by_username(username)[0].id
    idu1 = answer.find_by_id(ida).idu

    notification = Notification()
    notification.newupvote(ida=ida, idu1=idu1, idu2=idu2)
    return 'success'


'''
para: username, content, reason
举报事件
update: notification
'''
@notification.route('/tipoff', methods=['POST'])
def new_tipoff():
    username = request.form.get('username')
    content = request.form.get('content')
    reason = request.form.get('reason')

    notification = Notification()
    notification.newtipoff(username=username, content=content, reason=reason)
    return 'success'