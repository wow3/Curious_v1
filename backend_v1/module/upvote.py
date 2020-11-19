# module.upvote

from sqlalchemy import Table
from common.database import dbconnect
from module.user import User

dbsession, md, DBase = dbconnect()

class Upvote(DBase):
    __table__ = Table('upvote', md, autoload=True)


# ------------------------------查询类-------------------------------------

    # 根据用户id，问题id查询，用于解决重复点赞
    def find_by_iduida(self, idu, ida):
        result = dbsession.query(Upvote).filter_by(idu=idu, ida=ida).all()
        return result



# ------------------------------提交类-------------------------------------

    # 新增点赞数据
    def add(self, idu, ida):
        upvote = Upvote(idu=idu, ida=ida)
        dbsession.add(upvote)
        dbsession.commit()
        return 1