from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from wtforms.widgets import ColorInput


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    due_date = DateTimeField('Due Date', validators=[Optional()], format='%Y-%m-%d %H:%M')
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Save Task')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(max=200)])
    color = StringField('Color', widget=ColorInput(), default='#007bff')
    submit = SubmitField('Save Category')