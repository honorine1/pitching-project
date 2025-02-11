from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    comment = db.relationship('Comments',backref = 'user',lazy = "dynamic")
    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
   

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
       self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

def __repr__(self):
        return f'User {self.username}'

class Comments(db.Model):
    

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    # image_path = db.Column(db.String)
    pitch_comment = db.Column(db.String)
    postdate = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    pitches_id = db.Column(db.Integer,db.ForeignKey("pitches.id"))
    
    def save_comments(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitches_id=id).all()
        return comments

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer,primary_key=True)
    category = db.Column(db.String(255))
    pitches = db.relationship('Pitch',backref = 'categories', lazy='dynamic')
    # description = db.Column(db.String(255))

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls,id):
        categories = Category.query.all()
        # category = Category.query.filter_by(id=id).first()
        return categories


class Pitch(db.Model):
    

    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    # image_path = db.Column(db.String)
    pitch_content = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comments',backref = 'pitches', lazy='dynamic')
    category_id = db.Column(db.Integer,db.ForeignKey("categories.id"))
    # vote = db.relationship("votes",backref="pitches",lazy = "dynamic")


    def save_pitch(self):
        db.session.add(self)  
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        # pitches = Pitch.query.order_by(pitch_id=id).pitch().all()
        return pitches
