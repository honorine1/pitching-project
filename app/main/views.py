
from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import PitchForm,CommentForm,CategoryForm
from ..models import  User,Pitch,Comments,Category
from .forms import PitchForm, CommentForm
from flask_login import login_required, current_user
from .. import db
import datetime



# DISPLAY CATEGORIES IN THE LANDING PAGE
@main.route('/')
def index():


    '''
    View root page function that returns the index page and its data
    '''

    category = Category.get_categories(id) 
  

    title = 'Home - Welcome '
    return render_template('index.html', title = title,categories=category)

@main.route('/add/pitch')
def new_pitch():
    form=PitchForm()
    category = Category.query.filter_by(id=id).first()
    if category is None:
        abort(404)
    
    if form.validate_on_submit():
        pitch_content=form.pitch_content.data
        new_pitch = Pitch(pitch_content=pitch_content,category_id= category.id,user_id=current_user.id) 
        new_pitch.save_pitch()
        return redirect(url_for('.category', id= category.id))
    return render_template('newPitch.html',Pitch_form = form, category=category)

@main.route('/categories/<int:id>')
def category(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)

    pitches = Pitch.get_pitches(id)
    return render_template('category.html',pitches=pitches,category=category)

@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    form = CategoryForm()
    category=form.category.data
    
    if form.validate_on_submit():
        new_category = Category(category=category)
        new_category.save_category()

        return redirect(url_for('.new_pitch'))

    title = 'New category'
    return render_template('new_category.html',category_form = form,title=title)


# @main.route('/viewPitch/<int:id>', methods=['GET','POST'])
# @login_required
# def viewPitch(id):
#     '''
#     Function the returns a single pitch for comment to be added
#     '''

#     print(id)
#     pitches = Pitch.query.get(id)
#     if pitches is None:
#         abort(404)

#     comment = comments.get_comments(id)
#     return render_template('viewPitch.html',pitches=pitches, comment=comment, category_id=id)



# add comment

@main.route('/writeComment/<int:id>',methods=['GET','POST'])
@login_required
def leaveComment(id):
    form = CommentForm()
    title = 'Leave comment'
    pitches = Pitch.query.filter_by(id=id).first()


    if pitches is None:
        abort(404)
    if form.validate_on_submit():
        pitch_comment = form.pitch_comment.data
        new_comment = Comments(pitch_comment=pitch_comment,user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.viewPitch',id=pitches.id))

    return render_template('leaveComment.html',CommentForm=form, title=title)

  


