# module.question

from sqlalchemy import Table
from common.database import dbconnect
from module.user import User

dbsession, md, DBase = dbconnect()

class Question(DBase):
    __table__ = Table('question', md, autoload=True)

# -------------------------查询类----------------------------------

    # 查询所有问题
    def find_all(self):
        result = dbsession.query(Questoin).all()
        return result

    # 查询所有没有回答的问题
    def find_all_blank(self):
        result = dbsession.query(Question).filter_by(answer_count = 0).all()
        return result

    # 根据问题id查询问题
    def find_by_id(self, id):
        row = dbsession.query(Question).filter_by(id = id).first()
        return row

    # 根据用户id查询问题
    def find_by_idu(self, idu):
        result = dbsession.query(Question).filter_by(idu=idu).all()
        return result

    # 根据分类查询问题
    def find_by_category(self, category):
        result = dbsession.query(Question).filter_by(category=category).order_by(Question.view_count.desc()).all()
        return result

    # 根据分类查询并分页返回问题
    def find_limit_by_category(self, category, page, count):
        start = page*count      # 起点计算
        result = dbsession.query(Question).filter_by(category=category)\
            .order_by(Question.view_count.desc()).limit(count).offset(start).all()
        return result

    # 根据关键字查询问题
    def find_by_searchkey(self, key):
        result = dbsession.query(Question).filter(Question.title.like('%{key}%'.format(key=key))).all()
        return result




# -------------------------提交类----------------------------------

    # 用户提交问题
    def add_question(self, username, title, description, category):
        user = User()
        res = user.find_by_username(username)   # 根据用户名找到用户id
        # print(res[0].id)
        idu = res[0].id
        question = Question(idu=idu, title=title, category=category, description=description, view_count=0, answer_count=0, collect_count=0)
        dbsession.add(question)
        dbsession.commit()
        return 1

    # 问题被收藏，collect_count字段+1
    def add_collect_count(self, idq):
        question = dbsession.query(Question).filter_by(id=idq).first()
        question.collect_count += 1
        dbsession.commit()
        return 1

    # 问题被浏览，view_count字段+1
    def add_view_count(self, idq):
        question = dbsession.query(Question).filter_by(id=idq).first()
        question.view_count += 1
        dbsession.commit()
        return 1

    # 问题被回答，answer_count字段+1
    def add_answer_count(self, idq):
        question = dbsession.query(Question).filter_by(id=idq).first()
        question.answer_count += 1
        dbsession.commit()
        return 1






# # test1
# question = Question()
# question.add_question('222222@fake.com', '科比如果优化自己的出手选择，他会比原来的自己更强吗？',
#                       '科比如果优化自己的出手选择，他会比原来的自己更强吗？', '体育')

# # test2
# question = Question()
# res = question.find_limit_by_category('technology', 0, 5)
# for q in res:
#     print(q.title)