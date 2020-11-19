# module.notification

from sqlalchemy import Table
from common.database import dbconnect
from module.user import User
from module.question import Question
from module.answer import Answer

dbsession, md, DBase = dbconnect()

class Notification(DBase):
    __table__ = Table('notification', md, autoload=True)


# -------------------------------查询类-----------------------------------

    # 按用户id查询notification（已读）
    def find_by_idu_1(self, idu):
        result = dbsession.query(Notification).filter_by(idu=idu, read='y').all()
        return result

    # 按用户id查询notification（未读）
    def find_by_idu_0(self, idu):
        result = dbsession.query(Notification).filter_by(idu=idu, read='n').all()
        return result

    # 管理员获取未处理的举报信息
    def find_tip0(self):
        result = dbsession.query(Notification).filter_by(idu=0, read='n').all()
        return result

# -------------------------------提交类-----------------------------------

    # 新增问题回答消息，提示您的问题xxx有新的回答了，快去看看吧
    def newanswer(self, idq, idu):
        question = Question()
        title = question.find_by_id(id=idq).title
        content = "您的问题"+"'"+title+"'"+"有新的回答了，快去看看吧。"
        read = "n"

        notification = Notification(idu=idu, read=read, content=content)
        dbsession.add(notification)
        dbsession.commit()
        return 1

    # 新增回答被点赞消息，提示xxx点赞了您关于问题xxx的回答，点赞施加者idu2
    def newupvote(self, ida, idu1, idu2):
        answer = Answer()
        question = Question()
        user = User()

        nickname = user.find_by_id(idu2).nickname

        idq = answer.find_by_id(id=ida).idq

        title = question.find_by_id(id=idq).title

        content = nickname+"点赞了"+"您关于问题"+"'"+title+"'"+"的回答。"
        read = "n"

        notification = Notification(idu=idu1, read=read, content=content)
        dbsession.add(notification)
        dbsession.commit()
        return 1

    # 新增举报信息
    def newtipoff(self, username, content, reason):
        tip = " '" + username + "' " + "的言论" + " [" + content + "] " + "涉嫌" + " [" + reason + "] " + "，请查阅处理。"
        read = "n"
        idu = 0
        notification = Notification(idu=idu, read=read, content=tip)
        dbsession.add(notification)
        dbsession.commit()
        return 1



    # 将消息更新为已读
    def isread(self, id):
        notification = dbsession.query(Notification).filter_by(id=id).first()
        notification.read = 'y'
        dbsession.commit()
        return 1

