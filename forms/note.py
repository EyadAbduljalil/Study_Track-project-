from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class NoteForm(FlaskForm):
    """Form for creating and editing notes."""
    title = StringField('عنوان الملاحظة', validators=[DataRequired(), Length(min=3, max=100)])
    content = TextAreaField('محتوى الملاحظة', validators=[DataRequired()])
    submit = SubmitField('حفظ')

class ShareNoteForm(FlaskForm):
    """Form for sharing notes with other users."""
    email = EmailField('البريد الإلكتروني للمستخدم', validators=[DataRequired(), Email()])
    submit = SubmitField('مشاركة')
