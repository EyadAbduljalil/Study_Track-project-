from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class CourseForm(FlaskForm):
    """Form for creating and editing courses."""
    title = StringField('عنوان المقرر', validators=[DataRequired(), Length(min=3, max=100)])
    code = StringField('رمز المقرر', validators=[Length(max=20)])
    instructor = StringField('اسم المدرس', validators=[Length(max=100)])
    color = SelectField('اللون', choices=[
        ('#3498db', 'أزرق'),
        ('#2ecc71', 'أخضر'),
        ('#e74c3c', 'أحمر'),
        ('#f39c12', 'برتقالي'),
        ('#9b59b6', 'بنفسجي'),
        ('#1abc9c', 'فيروزي'),
        ('#34495e', 'رمادي داكن')
    ])
    submit = SubmitField('حفظ')
