# controller.upvote

from flask import Blueprint, make_response, request, jsonify
from module.answer import Answer
from module.user import User
from module.upvote import Upvote

upvote = Blueprint('upvote', __name__)


'''
para: username, ida 
新增回答点赞记录
update: update, answer
'''
@upvote.route('/addupvote', methods=['POST'])
def add_upvote():
    upvote = Upvote()
    user = User()
    answer = Answer()

    username = request.form.get("username")
    ida = request.form.get("ida")
    idu = user.find_by_username(username)[0].id

    res = upvote.find_by_iduida(idu=idu, ida=ida)
    if len(res) > 0:
        return 'repeated'
    else:
        upvote.add(idu=idu, ida=ida)
        answer.add_upvote(id=ida)
        return 'success'




