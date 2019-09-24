

from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,RadioField,SubmitField,ValidationError
from wtforms.validators import Required,Email

class PitchForm(FlaskForm):
   pitch_content = TextAreaField('Your pitch')
   submit = SubmitField('submit')

class CommentForm():
   pitch_comment = TextAreaField('Write your comment')
   submit = SubmitField('submit')

class CategoryForm(FlaskForm):
   category = RadioField('Label', choices=[('interview', 'interview'),('science','science'), ('product', 'product'),('technology','technology'),('promotion', 'promotion'),('artist','artist')])
   submit = SubmitField('submit')


# class ReviewForm(FlaskForm):
#    title = StringField('Review title',validators=[Required()])
#    review = TextAreaField('Movie review', validators=[Required()])
#    submit = SubmitField('Submit')
# class UpdateProfile(FlaskForm):
#    bio = TextAreaField('Tell us about you.',validators = [Required()])
#    submit = SubmitField('Submit')


#    name =  StringField('Comment name',validators=[Required()])
#    comment = TextAreaField('Pitch comment')
#    submit = SubmitField('Submit')
# class UpdateProfile(FlaskForm):
#     bio = TextAreaField('Tell us about you.',validators = [Required()])
#     submit = SubmitField('Submit')