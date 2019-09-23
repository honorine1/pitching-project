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
    #password_secure = db.Column(db.String(255))
    
    #role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    profile_pic_path = db.Column(db.String())
    # password_secure = db.Column(db.String(255))
    
    comment = db.relationship('Comments',backref = 'user',lazy = "dynamic")
    pitches = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    vote = db.relationship("Votes", backref ="user", lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self,password):
        # self.pass_secure = generate_password_hash(password)
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        # return check_password_hash(self.pass_secure,password)
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'User {self.username}'


class Review(db.Model):
    

    __tablename__ = 'reviews'

    id = db.Column(db.Integer,primary_key = True)
    movie_id = db.Column(db.Integer)
    movie_title = db.Column(db.String)
    image_path = db.Column(db.String)
    movie_review = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,id):
        reviews = Review.query.filter_by(movie_id=id).all()
        return reviews


        


class comments(db.Model):
    

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
    name = db.Column(db.String(255))
    pitchDesc = db.Column(db.String(255))

    def save_category(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_categories(cls,id):
        categories = Category.query.filter_by(category_id=id).all()
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
    vote = db.relationship("votes",backref="pitches",lazy = "dynamic")


    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_pitches(cls):
        Pitch.all_pitches.clear()

    @classmethod
    def get_pitches(cls,id):
        pitches = Pitch.query.filter_by(category_id=id).all()
        return pitches
