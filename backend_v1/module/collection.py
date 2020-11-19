# module.collection

from sqlalchemy import Table
from common.database import dbconnect
from module.user import User
from module.question import Question

dbsession, md, DBase = dbconnect()

class Collection(DBase):
    __table__ = Table('collection', md, autoload=True)


# ---------------------查询类-------------------------------------

    # 根据idu查询收藏
    def find_by_idu(self, idu):
        result = dbsession.query(Collection).filter_by(idu=idu).all()
        return result


    # 根据idu, idq查询，避免重复收藏
    def find_by_iduidq(self, idu, idq):
        result = dbsession.query(Collection).filter_by(idu=idu, idq=idq).all()
        return result


# ---------------------提交类-------------------------------------

    # 提交收藏
    def add(self, idu, idq):
        collection = Collection(idu=idu, idq=idq)
        dbsession.add(collection)
        dbsession.commit()
        return 1

