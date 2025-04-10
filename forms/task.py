from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from datetime import datetime

class TaskForm(FlaskForm):
    """Form for creating and editing tasks."""
    title = StringField('عنوان المهمة', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('وصف المهمة')

    # ✅ هذا هو التعديل المهم لفتح محرر التاريخ والوقت في المتصفح
    due_date = DateTimeField(
        'تاريخ الاستحقاق',
        validators=[DataRequired()],
        format='%Y-%m-%dT%H:%M',  # تنسيق datetime-local
        default=datetime.now,
        render_kw={"type": "datetime-local"}  # 🔥 يفتح التقويم + الساعة مباشرة
    )

    priority = SelectField('الأولوية', choices=[
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية')
    ], default='medium')

    status = SelectField('الحالة', choices=[
        ('pending', 'قيد الانتظار'),
        ('in_progress', 'قيد التنفيذ'),
        ('completed', 'مكتملة')
    ], default='pending')

    # 🔥 لازم نحط coerce=int عشان يشتغل مع الـ SelectField بشكل سليم
    course_id = SelectField('المقرر', coerce=int)

    submit = SubmitField('حفظ')
