# module.history

from sqlalchemy import Table
from common.database import dbconnect
from module.user import User
from module.question import Question

dbsession, md, DBase = dbconnect()

class History(DBase):
    __table__ = Table('history', md, autoload=True)


# ---------------------查询类-------------------------------------

    # 根据idu查询历史记录
    def find_by_idu(self, idu):
        result = dbsession.query(History).filter_by(idu=idu).all()
        return result


# ---------------------提交类-------------------------------------

    # 提交历史记录
    def add(self, idu, idq):
        history = History(idu=idu, idq=idq)
        dbsession.add(history)
        dbsession.commit()
        return 1