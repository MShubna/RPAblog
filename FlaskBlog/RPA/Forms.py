from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired,Email
#from FlaskBlog.Model_s import Rpacat, Rpaarea
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import  DecimalRangeField

class RpaForm(FlaskForm):
    title = StringField('What is the name of task/process you would like to recommend for automation?', validators=[DataRequired()])
    content = TextAreaField('Please provide a short description of task/process named above.', validators=[DataRequired()])
    area = SelectField('Automation Area',  coerce=int)
    cat = SelectField('Automation Category', coerce=int)
#    cat = SelectField ( )
#    cat1 = QuerySelectField( 'query category', query_factory=lambda : Rpacat.query)
    subcat = SelectField('Automation SubCategory', coerce=int)
    rulebaserate = DecimalRangeField( ' How rule-based is your task?', default=3 )
    indatarate = DecimalRangeField( ' How would you describe the input data for your task/process?',default=3 )
    indatastructrate = DecimalRangeField( ' How would you describe the  structure of your input data?',default=3 )
    changesrate = DecimalRangeField( ' Are you expect any changes in your process in the following 6 months?',default=3 )
    b = BooleanField('Do you have any documentation regarding this process/activity?')
    doc1 = BooleanField( 'YES - Detailed Work Instructions')
    doc2 = BooleanField( 'YES - Standard Operating Procedure')
    doc3 = BooleanField( 'YES - Task/Process maps/flowcharts')
    doc4 = BooleanField( 'YES - Input/Output Files' )
    email = StringField( 'Indicate email adress ',
                         validators=[DataRequired(),Email()])

    submit = SubmitField('Save')



