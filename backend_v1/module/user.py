# module.user
import random


from sqlalchemy import Table
from common.database import dbconnect

dbsession, md, DBase = dbconnect()

class User(DBase):
    __table__ = Table('user', md, autoload=True)

# ----------------------------查询类----------------------------------------

    # 查询所有用户
    def find_all(self):
        result = dbsession.query(User).all()
        return result

    # 根据用户id查询用户
    def find_by_id(self, id):
        row = dbsession.query(User).filter_by(id = id).first()
        return row

    # 查询用户名，判断注册时用户名是否已注册，也可用于登录校验
    def find_by_username(self, username):
        result = dbsession.query(User).filter_by(username=username).all()
        return result

# ----------------------------提交类----------------------------------------

    # 实现注册，用户名，密码
    def do_register(self, username, nickname, password):
        avatar = str(random.randint(1, 15))     # 头像库随机选择一张
        user = User(username=username, password=password, nickname=nickname, avatar_url=avatar+'.png', banned='正常')
        dbsession.add(user)
        dbsession.commit()
        return user

    # 封禁用户
    def do_ban(self, username):
        row = dbsession.query(User).filter_by(username=username).first()
        row.banned = '已封禁'
        dbsession.commit()
        return 1

    # 解禁用户
    def unban(self, username):
        row = dbsession.query(User).filter_by(username=username).first()
        row.banned = '正常'
        dbsession.commit()
        return 1
