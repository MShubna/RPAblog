from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()],render_kw= {"placeholder": "title of post"})
    content = TextAreaField('Content', validators=[DataRequired()],render_kw= {"placeholder": "content of post"})
    submit = SubmitField('Save')


