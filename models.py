from exts import db

#用户信息表
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    phone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(255),nullable=False)

#用户发布内容
class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    imgurl = db.Column(db.String(255), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship("User",backref=db.backref('questions'))


#评论详情
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    question = db.relationship("Question",backref=db.backref('comments'))
    author = db.relationship("User",backref=db.backref('comments'))
