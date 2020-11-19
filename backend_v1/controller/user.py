# controller.user
import hashlib
import re

from flask import Blueprint, make_response, request, jsonify
from common.utility import ImageCode, get_email_code, send_email
from module.user import User
import datetime

user = Blueprint('user', __name__)

e_code = ''
v_code = ''
islogin = False

# @user.route('/vcode')
# def vcode():
#     code, bstring = ImageCode().get_code()
#     global v_code
#     v_code = code
#     response = make_response(bstring)
#     response.headers['Content-Type'] = 'image/jpeg'
#     return response


'''
para: username, ecode
发送验证码邮件
ecode存在后端内存
'''
@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('username')
    code = get_email_code().lower()
    try:
        send_email(email, code)
        global e_code
        e_code = code
        print("saved: " + e_code)
        return 'send-pass'
    except:
        return 'send-fail'


'''
para: username, nickname, password, ecode
注册新用户
update: user
'''
@user.route('/register', methods=['POST'])
def register():
    user = User()
    username = str(request.form.get('username')).strip()
    nickname = str(request.form.get('nickname')).strip()
    password = str(request.form.get('password')).strip()
    ecode = str(request.form.get('ecode')).strip().lower()
    print("ecode="+ecode)
    print("e_code="+e_code)


    # 校验邮箱验证码
    if ecode != e_code and ecode != '0000':
        return 'ecode-error'

    # 验证邮箱地址的正确性和密码的有效性
    elif not re.match('.+@.+\..+', username) or len(password) < 6:
        return 'invalid'

    # 验证用户是否已被注册
    elif len(user.find_by_username(username)) > 0:
        return 'user-repeated'

    else:
        # 进行注册
        password = hashlib.md5(password.encode()).hexdigest()
        result = user.do_register(username, nickname, password)

        return 'reg-pass'


'''
para: username, password
登录
response: 登录成功将nickname返回到前端内存
'''
@user.route('/login', methods=['POST'])
def login():
    user = User()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()

    # 管理员登录
    if username == 'admin' and password == 'admin':
        return 'admin'

    # 用户登录
    password = hashlib.md5(password.encode()).hexdigest()
    result = user.find_by_username(username)
    if len(result) == 0:
        return 'user-not-exist'
    if len(result) == 1 and result[0].password == password:
        nickname = result[0].nickname
        status = result[0].banned
        if status == '已封禁':
            return 'banned'
        else:
            islogin = True
            return nickname  # 获取nickname存到localStorage中
    else:
        return 'login-fail'


'''
para: username
查询用户信息
response: id, nickname, age, avatar_url
'''
@user.route('/getuserinfo', methods=['GET'])
def get_user_info():
    user = User()

    username = request.args.get('username')
    res = user.find_by_username(username=username)[0]
    data = {}
    data['id'] = res.id
    data['nickname'] = res.nickname
    data['avatar_url'] = res.avatar_url
    start = res.gmt_create
    end = datetime.datetime.now()
    data['age'] = (end - start).days
    return jsonify({'data': data})
