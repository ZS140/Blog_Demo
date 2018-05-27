import datetime
from init_ import db


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    profession = db.Column(db.String(20))
    year = db.Column(db.Integer)
    sex = db.Column(db.String(2))
    city = db.Column(db.String(2))
    birthday = db.Column(db.DateTime)
    introduce = db.Column(db.Text(300))
    last = db.Column(db.DateTime)
    def is_active(self):
        return True
    def is_authenticated(self):#如果用户被认证，这个属性应该返回TRUE，即他们提供了有效的凭证。
        return True
    def get_id(self):
        return self.id
    @classmethod
    def login_check(cls,check_name,check_password):
        user = cls.query.filter(db.and_(User.name == check_name,User.password == check_password)).first()
        if user:
            return user
        else:
            None
class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime,default=datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer,db.ForeignKey('Users.id'))