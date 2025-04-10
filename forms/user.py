from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class EditProfileForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('البريد الإلكتروني', validators=[DataRequired(), Email()])
    submit = SubmitField('تحديث')

