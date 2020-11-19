# module.answer

from sqlalchemy import Table
from common.database import dbconnect
from module.user import User
from module.question import Question

dbsession, md, DBase = dbconnect()

class Answer(DBase):
    __table__ = Table('answer', md, autoload=True)


# ----------------------------------查询类------------------------------------

    # 根据id查找answer
    def find_by_id(self, id):
        row = dbsession.query(Answer).filter_by(id=id).first()
        return row

    # 按照问题id查找回答
    def find_by_idq(self, idq):
        result = dbsession.query(Answer).filter_by(idq=idq).order_by(Answer.upvote).all()
        return result

    # 按照用户id查找回答
    def find_by_idu(self, idu):
        result = dbsession.query(Answer).filter_by(idu=idu).all()
        return result

    # 按照用户id查询回答数量
    def count_by_idu(self, idu):
        result = dbsession.query(Answer).filter_by(idu=idu).count()
        return result

    # 按照用户id查询获赞数量
    def count_upvote_by_idu(self, idu):
        result = dbsession.query(Answer).filter_by(idu=idu).all()
        count = 0
        for res in result:
            count += res.upvote
        return count

    # 查询平均回答数量
    def count_avg(self):
        nUser = dbsession.query(User).count()
        nAnsewr = dbsession.query(Answer).count()
        avg_answer = round(nAnsewr/nUser, 2)
        return avg_answer

    # 查询平均获赞数量
    def count_avg_upvote(self):
        nUser = dbsession.query(User).count()
        result = dbsession.query(Answer).all()
        nUpvote = 0
        for res in result:
            nUpvote += res.upvote
        avg_upvote = round(nUpvote/nUser, 2)
        return avg_upvote



# ----------------------------------提交类------------------------------------

    # 针对idq提交回答
    def add_answer(self, idq, idu, content):
        answer = Answer(idq=idq, idu=idu, content=content, upvote=0)
        dbsession.add(answer)
        dbsession.commit()
        return 1


    # 回答被点赞
    def add_upvote(self, id):
        answer = dbsession.query(Answer).filter_by(id=id).first()
        answer.upvote += 1
        dbsession.commit()
        return 1
